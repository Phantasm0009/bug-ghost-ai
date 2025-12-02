"""GitHub OAuth minimal integration."""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.db.session import get_db
from app.models.user import User
import httpx

router = APIRouter(prefix="/api/auth", tags=["auth"]) 


@router.get("/github/login")
async def github_login():
    """Redirect to GitHub OAuth authorization page."""
    client_id = settings.GITHUB_CLIENT_ID
    if not client_id:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")
    redirect_uri = settings.GITHUB_REDIRECT_URI
    scope = "read:user user:email"
    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )
    return RedirectResponse(url)


@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    """Exchange code for access token and upsert user."""
    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")

    async with httpx.AsyncClient(headers={"Accept": "application/json"}) as client:
        # Exchange code
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI,
            },
        )
        token_resp.raise_for_status()
        token_json = token_resp.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="OAuth token exchange failed")

        # Fetch user profile
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_resp.raise_for_status()
        user_json = user_resp.json()
        gh_id = user_json.get("id")
        login = user_json.get("login")
        name = user_json.get("name")
        avatar_url = user_json.get("avatar_url")

        if not gh_id or not login:
            raise HTTPException(status_code=400, detail="Invalid GitHub user payload")

        # Upsert user
        user = db.query(User).filter(User.github_id == gh_id).first()
        if not user:
            user = User(github_id=gh_id, username=login, name=name, avatar_url=avatar_url)
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update profile fields if changed
            user.username = login
            user.name = name
            user.avatar_url = avatar_url
            db.commit()

    # For MVP: return user + access_token (frontend can store). In production, issue JWT httpOnly cookie.
    return {
        "user": {
            "id": str(user.id),
            "github_id": user.github_id,
            "username": user.username,
            "name": user.name,
            "avatar_url": user.avatar_url,
        },
        "github_access_token": access_token,
    }
