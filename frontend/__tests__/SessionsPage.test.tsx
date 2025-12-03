import { render, screen } from '@testing-library/react';
import SessionsPage from '@/app/sessions/page';

jest.mock('@/lib/api', () => ({
  __esModule: true,
  default: {
    get: jest.fn().mockResolvedValue({ data: [] }),
  },
}));

describe('SessionsPage', () => {
  it('shows empty state when no sessions', async () => {
    render(<SessionsPage />);
    expect(await screen.findByText(/No sessions yet/i)).toBeInTheDocument();
  });
});
