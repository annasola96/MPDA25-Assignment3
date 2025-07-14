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

#create a list composed of the lenghts of the lists in sp_idx
for i in range(len(sp_idx)):
    length.append(len(sp_idx[i]))



remap_length = []

#remap the numbers of the list named length from a domain from its minimum to its maximum to a domain from 0 to 50, amd append the results in remap_length
for i in range(len(length)):
    remap_num = (length[i] - min(length)) / (max(length) - min(length)) * 50
    remap_length.append(remap_num)

#create a list of lists of faces of the mesh m according to the indices of sp_idx
sp_faces_lists = []
for i in range(len(sp_idx)):
    sp_faces=[]
    for j in range(len(sp_idx[i])):
        sp_faces.append(m.Faces[sp_idx[i][j]])
    sp_faces_lists.append(sp_faces)


sp_faces_lists_gh = th.list_to_tree(sp_faces_lists)


# Create a list to store the strips (welded meshes)
strips = []
breps = []
unrolled_strips = []
unrolled_vertices = []

for faces in sp_faces_lists:
    # Create a new mesh
    mesh_strip = rg.Mesh()

    for vertex in initial_vertices:
        mesh_strip.Vertices.Add(vertex)
    
    # Add each face to the mesh
    for face in faces:
            # Add the face to the mesh
            mesh_strip.Faces.AddFace(face.A, face.B, face.C)
    
    #cull unused vertices of the mesh
    #mesh_strip.CullUnusedVertices()
    
    brep_strip = rg.Brep.CreateFromMesh(mesh_strip, True)
    unrolled = rg.Unroller(brep_strip)

    # Perform the unrolling
    unrolled_breps, unrolled_curves, unrolled_points, unrolled_dots = unrolled.PerformUnroll()
    joined_brep = rg.Brep.JoinBreps(unrolled_breps, 0.1)
    
    # Append the welded mesh to the list
    strips.append(mesh_strip)
    breps.append(brep_strip)
    unrolled_strips.extend(joined_brep)

    for brep in joined_brep:
        vertices = []
        for vertex in brep.Vertices:
            point = vertex.Location
            vertices.append(point)
        unrolled_vertices.append(vertices)

# Convert the list of lists to a Grasshopper data tree
unrolled_vertices_gh = th.list_to_tree(unrolled_vertices)



#fitted_lines = []

#for pts in unrolled_vertices:
    # Use Rhino's Line.TryFitLineToPoints method to fit a line
    #success, line = rg.Line.TryFitLineToPoints(pts, 0.01)  # Tolerance can be adjusted
    #if success:
    #    fitted_lines.append(line)
    #else:
    #    fitted_lines.append(None)  # Handle the failure case as needed

#for vertices in unrolled_vertices:
#    success, line = rg.Line.TryFitLineToPoints(vertices, 0.01)
#    if success:
#        fitted_lines.append(line)
#    else:
#        fitted_lines.append(None)  # Or handle the failure case as needed
