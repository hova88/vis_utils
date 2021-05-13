import numpy as np 

def get_pts_in_box3d(points , boxes):
    """
    :param 
        points: (#points,3/4)
        boxes: (N,7)
    :return:
        pt_in_box3d: (n, 3/4)
    """
    condition = (np.abs(points[:,0])  < 0.2) \
              * (np.abs(points[:,1])  < 0.2) \
              * (np.abs(points[:,2])  < 5) 

    for box in boxes:
        cx,cy,cz,dx,dy,dz,rz = box[:7]
        
        local_z = points[:,2] - cz
        cosa = np.cos(-rz) 
        sina = np.sin(-rz)
        local_x = (points[:,0] - cx) * cosa + (points[:,1] - cy) * (-sina)
        local_y = (points[:,0] - cx) * sina + (points[:,1] - cy) * cosa
        
        # Finding the intersection 
        condition += (np.abs(local_z)  < dz/2) \
                   * (np.abs(local_y ) < dy/2) \
                   * (np.abs(local_x ) < dx/2) 

    return points[condition] , points[~condition]


