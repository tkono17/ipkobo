#------------------------------------------------------------------------
# ipbox: CMakeLists.txt
#------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.10)
set(PROJECT_NAME ipbox)

project(${PROJECT_NAME})

set(DESTINATION $ENV{SWDIR})
message("SWDIR = $ENV{SWDIR}")
set(CMAKE_INSTALL_PREFIX ${DESTINATION})

set(ScriptFiles scripts/ipapp.py)

#------------------------------------------------------------------------
# Installation
#------------------------------------------------------------------------
install(DIRECTORY ipbox
  DESTINATION python
  FILES_MATCHING PATTERN "*.py")

foreach(prog ${ScriptFiles})
  install(PROGRAMS ${prog} DESTINATION bin)
endforeach()

