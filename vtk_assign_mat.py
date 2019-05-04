#!/tools/python/2.6-x86_64/bin/python

import os
import sys

import re
from optparse import OptionParser, OptionValueError

import numpy as np

import glob
import vtk
from vtk.util import numpy_support

# so we can find our ../lib no matter how we are called
findbin = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(findbin + '/../lib')


# parse command line
p = OptionParser(usage="""usage: %prog [options] <top_solid> <material_number> <casename> <solid.vtu> <solids.dat> <joint_ele.dat> <out_file.vtu> 
Assign material properties according to the surfaces given in "solids.dat" file

Write new_*.ele and new_*.ine files


""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, .vtu output")
p.add_option("-m", action="store", dest="multikey", type="str", help="Multikey of the mesh partition.  If given, then <out_vtu> will contain cosflow_multikey")
(opts, args) = p.parse_args()


# Get the arguments
if len(args) != 6:
  print "Program must be called with 7 arguments"
  p.print_help()
  sys.exit(1)
#(top_solid, dummy_solid, casename, in_file, solid_file, joint_file, out_file) = args
#(top_solid, dummy_solid, casename, in_file, solid_file, joint_file, out_file) = args
(dummy_solid, casename, solid_vtu, solid_file, joint_file, out_file) = args

if not out_file.endswith(".vtu"):
  print "Out_vtu must end with .vtu"
  sys.exit(2)


solid_names = []
mat_names = []
mat_numbers = []


if opts.verbose: print "Reading solid file names"
f = open(solid_file, 'r')
for line in f:
  tuple = line.split()
  if not tuple:
    continue
  solid_names.append(tuple[0])
  mat_names.append(tuple[1])
  mat_numbers.append(tuple[2])

f.close()

joint_ele_mat_dict = {}


f = open(joint_file, 'r')
for line in f:
  tuple = line.split()
  if not tuple:
    continue
  mat_names.append(tuple[0])
  mat_numbers.append(tuple[1])
  if tuple[0] not in joint_ele_mat_dict:
    joint_ele_mat_dict[tuple[0]] = 0
f.close()

# number of solids = total - joint elements
num_solids = len(mat_names)-1

print "Number of layers " + str(num_solids)


#Store material names in a Dictonary which will be used later on
#when counting number of elements belong to specific material

mat_type_dict = {}

for i in range(len(mat_names)):
  mat_type_dict[mat_names[i]] = mat_numbers[i]

#print mat_type_dict.values()
#exit(0)

mat_list_dict = {}

for i in range(len(mat_names)):
  if mat_names[i] not in mat_list_dict:
    mat_list_dict[mat_names[i]] = 0

#print mat_type_dict['roofandfloorclos']
#exit(0)

# Get mesh
mesh_reader = vtk.vtkXMLUnstructuredGridReader()
mesh_reader.SetFileName(solid_vtu)
mesh_reader.Update()

mesh = mesh_reader.GetOutput()

if opts.verbose: print "Calculating the centroid of each element"
cc = vtk.vtkCellCenters()
cc.SetInputConnection(mesh.GetProducerPort())
cc.Update()
cc = cc.GetOutput()  # vtkUnstructuredGrid

# Read master ele file 
f = open(casename+".ele",'r')
master_ele_data = f.readlines()
f.close()

mat_list_array = vtk.vtkStringArray()
mat_list_array.SetName("cosflow_material_name")
mat_list_array.Resize(cc.GetNumberOfPoints())

#mat_num_array = vtk.vtkIntArray()
#mat_num_array.SetName("cosflow_material")
#mat_num_array.Resize(cc.GetNumberOfPoints())

#print mat_num_array.GetSize()
mat_num_array = mesh.GetCellData().GetArray("cosflow_material")
#mat_list_array = mesh.GetFieldData().GetArray("cosflow_material_name")
#print mat_num_array1.GetSize()

for i in range(len(master_ele_data)):
  line = master_ele_data[i].strip()
  tuple = line.split()
  mat_list_array.SetValue(i, tuple[0])
  mat_type_dict[tuple[0]]
  mat_num_array.SetValue(i, int(mat_type_dict[tuple[0]]))


loc = [vtk.vtkCellLocator() for x in range(num_solids)]

for sol in range(num_solids):
  sol_name = solid_names[sol]
  if opts.verbose: print "Reading", sol_name, "and building the locator"
  r = vtk.vtkXMLUnstructuredGridReader()
  r.SetFileName(sol_name)
  r.Update()
  loc[sol].SetDataSet(r.GetOutput())
  loc[sol].BuildLocator()


dummy_loc = vtk.vtkCellLocator()

if opts.verbose: print "Reading", dummy_solid, "and building the locator"
dummy_r = vtk.vtkXMLUnstructuredGridReader()
dummy_r.SetFileName(dummy_solid)
dummy_r.Update()
dummy_loc.SetDataSet(dummy_r.GetOutput())
dummy_loc.BuildLocator()

#top_limit_loc = vtk.vtkCellLocator()
#if opts.verbose: print "Reading", top_solid, "and building the locator"
#top_solid_r = vtk.vtkXMLUnstructuredGridReader()
#top_solid_r.SetFileName(top_solid)
#top_solid_r.Update()
#top_limit_loc.SetDataSet(top_solid_r.GetOutput())
#top_limit_loc.BuildLocator()


if opts.verbose: print "Prescribing material numbers to the mesh"
five_percent = cc.GetNumberOfPoints()/20

print "cc.GetNumberOfPoints()",cc.GetNumberOfPoints()


for cellid in range(cc.GetNumberOfPoints()):

  if (cellid+1)%five_percent == 0:
    print " ", str(int((100.0*cellid)/cc.GetNumberOfPoints())) + "%"
    #if material_array.GetValue(cellid) == -1:
  xyz = cc.GetPoint(cellid)

  #if top_limit_loc.FindCell(xyz) >= 0:
  #  mat_list_array.SetValue(cellid,mat_names[num_solids-1].strip())
  #  mat_num_array.SetValue(cellid,int(mat_numbers[num_solids-1].strip()))


#Assign material if the cell is above dummy surface and below top solid
  if dummy_loc.FindCell(xyz) >= 0 and int(mat_num_array.GetValue(cellid)) != int(mat_numbers[num_solids-1].strip()):
  #if int(mat_num_array.GetValue(cellid)) > int(mat_number) and int(mat_num_array.GetValue(cellid)) != int(mat_numbers[num_solids-1].strip()):
  #if int(mat_num_array.GetValue(cellid)) != int(mat_numbers[num_solids-1].strip()):
  #elif int(mat_num_array.GetValue(cellid)) != int(mat_numbers[num_solids-1].strip()):
    for sol in range(num_solids-2, -1, -1):
      if mat_list_array.GetValue(cellid) not in joint_ele_mat_dict: 
        if loc[sol].FindCell(xyz) >= 0:
      
          mat_list_array.SetValue(cellid,mat_names[sol].strip())
          mat_num_array.SetValue(cellid,int(mat_numbers[sol].strip()))
          break
        #else: #must have been really bad insersections, or min_thickness set too large - ele is below the bottom surface.  put to material=0
         # mat_list_array.SetValue(cellid,"Base")
         # mat_num_array.SetValue(cellid,0)

mesh.GetCellData().RemoveArray("cosflow_material")
mesh.GetCellData().AddArray(mat_num_array)

#mesh.GetFieldData().RemoveArray("cosflow_material_name")
#mesh.GetFieldData().AddArray(mat_list_array)


if opts.verbose: "Writing new master ele file"
f = open("new_"+casename+".ele", 'w')

for i in range (master_ele_data.__len__()):
  line = master_ele_data[i].strip()
  tuple = line.split()
  tuple[0] = mat_list_array.GetValue(i)
  line = ' '.join(tuple)
  f.write(line+'\n')
#f.writelines(new_master_ele_data)
f.close()

#mesh.GetCellData().AddArray(remove_array)
command_used = vtk.vtkStringArray()
command_used.SetName("provenance")
command_used.InsertNextValue(" ".join(sys.argv))
mesh.GetFieldData().AddArray(command_used)

#cn = vtk.vtkStringArray()
#cn.SetName("cosflow_casename")
#cn.InsertNextValue(solid_vtu)
#mesh.GetFieldData().AddArray(cn)

if opts.verbose: print "Reading modified master ele file"
f = open("new_"+casename+".ele", 'r')
data = f.readlines()
f.close()

for i in range(data.__len__()):
  line = data[i].strip()
  tuple = line.split()
  if tuple[0] in mat_list_dict:
    mat_list_dict[tuple[0]] += 1


#Read data in master.ine file
f = open(casename+'.ine', 'r')
data = f.readlines()
f.close()


if opts.verbose: print "Updating master .ine file"
#Write modified *.ine file
data_write = []
string_check = "PROBLEM ELEMENTS"
s = ''
fout = open('new_'+casename+'.ine', 'w')

for i in range(data.__len__()):
  line = data[i].strip()
  tuple = line.split()

  l = str(tuple[0])+' '+ str(tuple[1])
  if (l == string_check):
    if tuple[2] in mat_list_dict:
      tuple[3] = str(mat_list_dict[tuple[2]])

  s = ' '.join(tuple)
  data_write.append(s+'\n')

fout.writelines(data_write)
fout.close()


if opts.verbose: print "Writing", out_file
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_file)


if opts.ascii:
   writer.SetDataModeToAscii()
else:
   writer.SetDataModeToBinary()

writer.SetInputConnection(mesh.GetProducerPort())
writer.Write()

print "DONE"
