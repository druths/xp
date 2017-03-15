# Change Log

## Unreleased

### Added

  * Running a marked task now triggers a warning that nothing was done (Issue #2)
  * Added the ability to change the forcing status with simple, short flags that can be used anywhere (Issue #7)
  * Support for referencing variables in other pipelines (Issue #15)
  * Support for omitting the .xp extension when using pipelines (Issue #18)
  * Support for making unmarkable tasks
  * Added support for task-level properties
  * Added support for simple tasks (tasks with a language suffix and a single block)
  * Added support for a configuration file
  * Added support for pluggable kernels

### Changed

  * Modularized the handling of code block implementations.
  * Reimplemented entire backend execution system using class-based Kernels.

### Depricated

### Removed

	* CodeImpl class and all related code is gone (replaced by xp.kernels.base et al.)

### Fixed

  * A simple example analyzing world population (examples/world_pop) (Issue #10)

### Security
