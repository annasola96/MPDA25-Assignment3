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

for faces in sp_faces_lists:
    # Create a new mesh
    mesh = rg.Mesh()
    
    # Add each face to the mesh
    for face in faces:
        # Add the vertices of the face to the mesh
        for vertex_index in [face.A, face.B, face.C]:
            mesh.Vertices.Add(m.Vertices[vertex_index])
        
        # Add the face to the mesh
            mesh.Faces.AddFace(face.A, face.B, face.C)
    
#     # Weld the mesh
    mesh.Weld(0.0001)  # 0.01 is the tolerance, adjust as needed
    
#     # Append the welded mesh to the list
    strips.append(mesh)

