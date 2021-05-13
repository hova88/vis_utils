import numpy as np 
import open3d as o3d 

from .src import create_box , create_coordinate , create_arrow , get_pts_in_box3d

class PointCloudVis(object):
    def __init__(self):
        self.colorbar = [[1,0,0],[0,1,0],[0,0,1]]

    @staticmethod
    def get_points(vis , pts , color= [0.5 , 0.5 , 0.5]):
        colors = [color] * pts.shape[0]
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(pts[:,:3])
        pc.colors = o3d.utility.Vector3dVector(colors)
        vis.add_geometry(pc)

    @staticmethod
    def get_boxes(vis , boxes , color= [0.5 , 0.5 , 0.5]):
        boxes_o3d = []
        for box in boxes:
            box_o3d = create_box(box , color)
            boxes_o3d.append(box_o3d)
        [vis.add_geometry(element) for element in boxes_o3d] 

    @staticmethod
    def get_arrow(vis , boxes, color=[0.5 , 0.5 , 0.5]):
        arrows = []
        for box in boxes:
            x,y,z,l = box[:4]
            yaw = box[6]
            # get direction arrow
            dir_x = l / 2.0 * np.cos(yaw)
            dir_y = l / 2.0 * np.sin(yaw)

            arrow_origin = [x - dir_x, y - dir_y, z]
            arrow_end = [x + dir_x, y + dir_y, z]
            arrow = create_arrow(arrow_origin, arrow_end, color)
            arrows.append(arrow)
        [vis.add_geometry(element) for element in arrows] 

    @staticmethod
    def get_boxes_with_arrow(vis , boxes, color=[0.5 , 0.5 , 0.5]):
        boxes_o3d = []
        for box in boxes:
            # create box
            box_o3d = create_box(box , color)
            # create direction arrow
            x,y,z,l = box[:4]
            yaw = box[6]
            dir_x = l / 2.0 * np.cos(yaw)
            dir_y = l / 2.0 * np.sin(yaw)
            arrow_origin = [x - dir_x, y - dir_y, z]
            arrow_end = [x + dir_x, y + dir_y, z]
            arrow = create_arrow(arrow_origin, arrow_end, color)

            boxes_o3d.append(box_o3d)
            boxes_o3d.append(arrow)

        [vis.add_geometry(element) for element in boxes_o3d] 


    def DRAW_CLOUD(self,clouds_list):
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        for cloud in clouds_list:
            # add point cloud with color
            self.get_points(vis , cloud )
            # add coordinate frame
            coordinate_frame = create_coordinate(size=2.0, origin=[0, 0, 0])
            vis.add_geometry(coordinate_frame)
            # drop the window
            vis.get_render_option().point_size = 2
            vis.run()
            vis.destroy_window()

    def DRAW_BOXES(self , clouds_list , boxes_list):

        assert len(clouds_list) == len(boxes_list)

        for i in range(len(clouds_list)):
            print("frame id : " , i)
            vis = o3d.visualization.Visualizer()
            vis.create_window()
            cloud = clouds_list[i]
            boxes = boxes_list[i]
            # 1. add point cloud with defulat color
            self.get_points(vis , cloud )

            # 2. add boxes / arrow / pts_in_boxes with color
            if isinstance(boxes , list):
                for ind in range(len(boxes)):
                    pts_in_box , _ = get_pts_in_box3d(cloud , boxes[ind])
                    self.get_points(vis , pts_in_box , self.colorbar[ind])
                    self.get_boxes_with_arrow(vis , boxes[ind] , self.colorbar[ind])
            else: 
                pts_in_box , _ = get_pts_in_box3d(cloud , boxes)
                self.get_points(vis , pts_in_box , self.colorbar[0])
                self.get_boxes(vis , boxes , self.colorbar[0])

            # 4. coordinate frame
            coordinate_frame = create_coordinate(size=2.0, origin=[0, 0, 0])
            vis.add_geometry(coordinate_frame)

            # 5. drop the window
            vis.get_render_option().point_size = 2
            vis.run()
            vis.destroy_window()

if __name__ == "__main__":
    
    V = PointCloudVis()
    pts = np.eye((3))
    boxes = np.array([0,0,0,1,1,1,0]).reshape(1,7)
    clouds_list = [pts]
    boxes_list = [[boxes , boxes , boxes]]
    V.DRAW_BOXES(clouds_list , boxes_list)
