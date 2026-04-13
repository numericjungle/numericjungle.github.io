# Jekyll source 
Read more here: [GitHub User Pages](https://help.github.com/articles/user-organization-and-project-pages).

## Development Setup

### Prerequisites

You need:
1. **Ruby >= 3.1.0** (for Jekyll and Bundler)
2. **Node.js/npm** (for JavaScript runtime)

### Quick Setup

**1. Install Ruby 3.2.2 using rbenv:**

```bash
# Install rbenv (Ruby version manager)
brew install rbenv ruby-build

# Initialize rbenv for bash
echo 'eval "$(rbenv init - bash)"' >> ~/.bash_profile
source ~/.bash_profile

# Install Ruby 3.2.2
rbenv install 3.2.2
rbenv global 3.2.2

# Verify
ruby -v  # Should show 3.2.2
```

**2. Install Node.js:**

```bash
# Option 1: Using Homebrew
brew install node

# Option 2: Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bash_profile
nvm install --lts
nvm use --lts
```

**3. Install Bundler and run the server:**

```bash
# Install Bundler
gem install bundler:2.6.6

# Run the development server
bash run-server.sh --drafts

# Run in production mode without drafts
bash run-server.sh --prod
```

The server will be available at http://localhost:4000

For detailed setup instructions and troubleshooting, see [SETUP_DEV_ENVIRONMENT.md](SETUP_DEV_ENVIRONMENT.md).

# License
The following directories and their contents are Copyright Sean Chang.  You may not reuse anything therein without my permission:

*   _posts/
*   _drafts/
*   images/ (unless otherwise noted in a watermark)

All other directories and files are MIT Licensed.
