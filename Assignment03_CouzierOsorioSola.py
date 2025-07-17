#r: networkx
#r: matplotlib

from typing import cast, Any
import networkx as nx # type: ignore
import matplotlib.pyplot as plt # type: ignore
import Rhino.Geometry as rg # type: ignore beaause using stubs
import ghpythonlib.treehelpers as th # type: ignore
import graph_helpers as graph 


# DECLARE INPUT VARIABLES OF PYTHON COMPONENT
m = cast(rg.Mesh, m)  # type: ignore
sp_idx = th.tree_to_list(cast(int, i))
#length_prio = cast(int, length_priority)

#get the list of vertices of m
initial_vertices = m.Vertices

length = []
sp_idx_several = []

#create a list composed of the lenghts of the lists in sp_idx and remove strips with only 1 face
for i in range(len(sp_idx)):
    length.append(len(sp_idx[i]))
    if len(sp_idx[i]) > 22:
        sp_idx_several.append(sp_idx[i])
    else:
        pass


remap_length = []

#remap the numbers of the list named length from a domain from its minimum to its maximum to a domain from 0 to 50, amd append the results in remap_length
for i in range(len(length)):
    remap_num = (length[i] - min(length)) / (max(length) - min(length)) * 50
    remap_length.append(remap_num)

#create a list of lists of faces of the mesh m according to the indices of sp_idx
sp_faces_lists = []
for i in range(len(sp_idx_several)):
    sp_faces=[]
    for j in range(len(sp_idx_several[i])):
        sp_faces.append(m.Faces[sp_idx_several[i][j]])
    sp_faces_lists.append(sp_faces)


# Create a list to store the unrolled strips (faces)
unrolled_strips_unjoined = []

for faces in sp_faces_lists:
    # Create a new mesh
    mesh_strip = rg.Mesh()

    for vertex in initial_vertices:
        mesh_strip.Vertices.Add(vertex)
    
    # Add each face to the mesh
    for face in faces:
        # Add the face to the mesh
        mesh_strip.Faces.AddFace(face.A, face.B, face.C)
    
    brep_strip = rg.Brep.CreateFromMesh(mesh_strip, True)
    unrolled = rg.Unroller(brep_strip)

    # Perform the unrolling
    unrolled_breps, unrolled_curves, unrolled_points, unrolled_dots = unrolled.PerformUnroll()
    unrolled_strips_unjoined.append(unrolled_breps)


centers_lists = []

for strip in unrolled_strips_unjoined:
    centers = []
    for face in strip:
        amp = rg.AreaMassProperties.Compute(face)
        centers.append(amp.Centroid)
    centers_lists.append(centers)

straightlines = []
#For each list of points of centers_lists, do a line from the first point to the last point
for centers in centers_lists:
    line = rg.Line(centers[0], centers[-1])
    straightlines.append(line)

avrg_distance = []

#For each point of each list of centers_lists, calculate the distance to the corresponding line of straightlines
for i in range(len(centers_lists)):
    distance_add = 0
    for j in range(len(centers_lists[i])):
        distance = straightlines[i].DistanceTo(centers_lists[i][j],True)
        distance_add += distance
    avrg_distance.append(distance_add / len(centers_lists[i]))

remap_avrg_distance = [0]

#remap the numbers of the list named avrg_distance from a domain from its minimum to its maximum to a domain from 0 to 50, and append the results in remap_avg_distance
for i in range(len(avrg_distance)):
    remap_num = (avrg_distance[i] - min(avrg_distance)) / (max(avrg_distance) - min(avrg_distance)) * 50
    remap_num = 50 - remap_num
    remap_avrg_distance.append(remap_num)


grade=[]

for i in range(len(remap_avrg_distance)):
    grade.append(remap_avrg_distance[i]+remap_length[i])

#get the index of the maximum number in grade
max_index = grade.index(max(grade))

chosen_path = sp_idx_several[max_index]