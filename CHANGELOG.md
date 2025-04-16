# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-04-16

### Added
- Added file base URL support in config (`DIFY_FILE_BASE_URL`)
- Added file URL handling with base URL support in File class
- Added config and files_base_url fields to Session class

### Changed
- Updated tool parameter conversion to support files_base_url
- Updated plugin initialization to set files_base_url