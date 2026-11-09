# Public CV privacy

- Always publish a sanitised CV without Cachan, a home address, or any phone number.
- The CV in `Documents/latex-projects/cv` is private input. Never copy its built PDF directly into this repository or a deployment.
- Build a separate public copy with the private contact line removed from the LaTeX source. Keep the private source unchanged.
- Before publishing, run `python3 scripts/check_public_cv.py assets/cv.pdf` and visually inspect the public PDF. Stop if extraction fails or private contact information is found.
- Keep the privacy check ahead of deployment in `.github/workflows/publish.yml`. Never bypass it.
- Preserve existing uncommitted work, use native apply_patch for manual source edits, and provide before/after comparisons. Leave the user's checkout unstaged and uncommitted unless requested.
