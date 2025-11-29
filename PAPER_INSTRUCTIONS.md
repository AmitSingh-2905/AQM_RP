# How to Compile the Research Paper

The file `bare_jrnl.tex` contains the source code for your IEEE research paper. Since you do not have a local LaTeX environment installed (missing `latexmk` and `pdflatex`), the easiest way to compile this into a PDF is using **Overleaf**.

## Option 1: Using Overleaf (Recommended)

1.  Go to [Overleaf.com](https://www.overleaf.com) and log in.
2.  Click **"New Project"** -> **"Blank Project"**.
3.  Name it (e.g., "AQM_Research_Paper").
4.  In the project, click the **Upload** icon (top left).
5.  Upload the `bare_jrnl.tex` file from your computer.
6.  (Optional) If you have any images (like `system_architecture.png`), upload them as well.
7.  Open `bare_jrnl.tex` in the editor and click **Recompile**.

Overleaf already has the `IEEEtran` class installed, so it should work immediately.

## Option 2: Building Locally on macOS

If you prefer to build it in VS Code, you need to install a LaTeX distribution:

1.  **Install MacTeX**:
    *   Download from [tug.org/mactex](https://www.tug.org/mactex/) (Note: It is a large download, ~4GB).
    *   Or install via Homebrew: `brew install --cask mactex`
2.  **Restart VS Code**: After installation, restart VS Code so it can find the `latexmk` command.
3.  **Download IEEEtran.cls**:
    *   You may need to download the `IEEEtran.cls` file from the [IEEE website](https://www.ieee.org/conferences/publishing/templates.html) and place it in the same folder as `bare_jrnl.tex`.
