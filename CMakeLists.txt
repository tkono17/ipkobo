#------------------------------------------------------------------------
# ipcat: CMakeLists.txt
#------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.10)
set(PROJECT_NAME ipcat)

project(${PROJECT_NAME})

set(DESTINATION $ENV{SWDIR})
message("SWDIR = $ENV{SWDIR}")
set(CMAKE_INSTALL_PREFIX ${DESTINATION})

set(ScriptFiles python/ipapp.py)

#------------------------------------------------------------------------
# Installation
#------------------------------------------------------------------------
install(DIRECTORY python/ipcat
  DESTINATION python
  FILES_MATCHING PATTERN "*.py")

foreach(prog ${ScriptFiles})
  install(PROGRAMS ${prog} DESTINATION bin)
endforeach()

