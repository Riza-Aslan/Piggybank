# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.3] - 2026-04-04

### Fixed
- Fixed infinite restart loop in run.sh by properly backgrounding the cronjob process
- Added curl timeouts to prevent hanging requests
- Added checks for python3 and uvicorn availability before execution
- Improved error handling to prevent crashes that trigger HA restart loop

## [1.2.2] - 2026-04-04

### Fixed
- Fixed recurring transaction execution logic to properly handle start dates in the past
- Fixed `next_execution` calculation to ensure first transaction is scheduled correctly
- Fixed `execute_due_recurring_transactions` to use scheduled date instead of current time for transaction date
- Fixed `update_recurring_transaction` to recalculate next execution from `last_executed` correctly

### Changed
- Switched from Python `requests` to `curl` in cronjob to avoid additional dependencies
- Added immediate check for due recurring transactions on startup (catches missed executions)
- Improved reliability of recurring transaction background process

### Added
- Automatic creation of first transaction when start date is in the past or today
- Recurring transactions (Abos) are now included in export and import
- Import now properly restores recurring transactions along with persons and transactions

## [1.2.1] - 2026-04-04

### Added
- Initial release with recurring transactions (Abos) feature
- Automatic execution of due recurring transactions every 12 hours
- Dashboard with account balances and monthly statistics
- Home Assistant integration with REST sensors
- Import/Export functionality
