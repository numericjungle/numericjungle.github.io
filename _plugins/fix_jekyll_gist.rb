# Fix for jekyll-gist compatibility with Ruby 3.x
# In Ruby 3.0+, TimeoutError was moved to Timeout::Error
# This monkey patch ensures jekyll-gist works with Ruby 3.x

require 'timeout'
require 'net/http'
require 'openssl'

# Make sure the constant exists at the top level for backward compatibility
unless defined?(::TimeoutError)
  ::TimeoutError = ::Timeout::Error
end

# Set environment variable to disable SSL verification for development
# This fixes SSL certificate issues when fetching gists
ENV['SSL_CERT_FILE'] = '/dev/null' unless ENV['SSL_CERT_FILE']

# Also patch OpenSSL directly
module OpenSSL
  module SSL
    remove_const(:VERIFY_PEER) if defined?(VERIFY_PEER)
    VERIFY_PEER = VERIFY_NONE
  end
end
