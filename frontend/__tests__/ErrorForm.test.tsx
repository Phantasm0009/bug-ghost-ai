import { render, screen, fireEvent } from '@testing-library/react';
import ErrorForm from '@/components/ErrorForm';

function renderForm() {
  return render(
    <ErrorForm
      onSubmitSuccess={() => {}}
      isLoading={false}
      setIsLoading={() => {}}
    />
  );
}

describe('ErrorForm', () => {
  it('shows validation messages when submitting empty', async () => {
    renderForm();
    fireEvent.click(screen.getByRole('button', { name: /generate reproduction/i }));
    expect(await screen.findByText(/Language is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/Error text is required/i)).toBeInTheDocument();
  });
});
