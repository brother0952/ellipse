import cv2
import numpy as np

def create_triple_eccentric_ring_gradient(
    size, 
    outer_center, outer_radius,
    middle_center, middle_radius,
    inner_center, inner_radius,
    outer_brightness,
    middle_brightness,
    inner_brightness
):
    """创建三重偏心圆环渐变
    
    Args:
        size: (width, height) 画布尺寸
        outer_center: (x, y) 外圆圆心位置
        outer_radius: 外圆半径
        middle_center: (x, y) 中间圆圆心位置
        middle_radius: 中间圆半径
        inner_center: (x, y) 内圆圆心位置
        inner_radius: 内圆半径
        outer_brightness: 外圆亮度值 (0-1)
        middle_brightness: 中间圆亮度值 (0-1)
        inner_brightness: 内圆亮度值 (0-1)
    """
    canvas = np.zeros(size, dtype=np.float32)
    y, x = np.ogrid[:size[0], :size[1]]
    
    # 计算到三个圆心的距离
    dist_from_outer = np.sqrt((x - outer_center[0])**2 + (y - outer_center[1])**2)
    dist_from_middle = np.sqrt((x - middle_center[0])**2 + (y - middle_center[1])**2)
    dist_from_inner = np.sqrt((x - inner_center[0])**2 + (y - inner_center[1])**2)
    
    # 定义有效区域：在外圆内，不在内圆内
    valid_mask = (dist_from_outer <= outer_radius) & (dist_from_inner >= inner_radius)
    
    if valid_mask.any():
        gradient = np.zeros_like(dist_from_outer)
        
        # 计算到各个圆边界的距离
        dist_to_inner = dist_from_inner - inner_radius
        dist_to_middle = np.abs(dist_from_middle - middle_radius)
        dist_to_outer = outer_radius - dist_from_outer
        
        # 计算总距离和比例
        total_dist = dist_to_inner + dist_to_middle + dist_to_outer
        
        # 在有效区域计算渐变
        valid_points = valid_mask
        if valid_points.any():
            # 计算每个点到三个圆的归一化距离
            w_inner = dist_to_inner[valid_points] / total_dist[valid_points]
            w_middle = dist_to_middle[valid_points] / total_dist[valid_points]
            w_outer = dist_to_outer[valid_points] / total_dist[valid_points]
            
            # 使用三个权重进行亮度插值
            gradient[valid_points] = (
                inner_brightness * w_inner +
                middle_brightness * w_middle +
                outer_brightness * w_outer
            )
        
        canvas[valid_mask] = gradient[valid_mask]
    
    return canvas

def check_circles_intersection(c1, r1, c2, r2):
    """检查两个圆是否相交
    
    Args:
        c1: (x, y) 第一个圆的圆心
        r1: 第一个圆的半径
        c2: (x, y) 第二个圆的圆心
        r2: 第二个圆的半径
    """
    dist = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    return dist < (r1 + r2)

def draw_frame():
    # 创建黑色画布 (480, 640)
    canvas = np.zeros((480, 640), dtype=np.float32)
    
    # 设置三个圆的参数，都使用相同的圆心
    center = (320, 240)  # 画布中心
    
    # 从外到内设置三个圆的半径，确保不相交
    outer_radius = 150
    middle_radius = 110  # 比外圆小，留出间隔
    inner_radius = 70   # 比中间圆小，留出间隔
    
    # 所有圆使用相同的圆心
    outer_center = (320, 240)
    middle_center = (320+20, 240+20)
    inner_center = (320+25, 240+25)
    
    # 检查圆是否相交
    circles = [
        (outer_center, outer_radius),
        (middle_center, middle_radius),
        (inner_center, inner_radius)
    ]
    

    # for i in range(len(circles)):
    #     for j in range(i + 1, len(circles)):
    #         if check_circles_intersection(circles[i][0], circles[i][1], 
    #                                    circles[j][0], circles[j][1]):
    #             print(f"Warning: Circles {i} and {j} intersect!")
                #return None
    
    # 创建三重同心圆环
    ring = create_triple_eccentric_ring_gradient(
        size=(480, 640),
        outer_center=outer_center,
        outer_radius=outer_radius,
        middle_center=middle_center,
        middle_radius=middle_radius,
        inner_center=inner_center,
        inner_radius=inner_radius,
        outer_brightness=0.9,    # 外圆亮度
        middle_brightness=0.7,   # 中间圆亮度
        inner_brightness=0.1     # 内圆亮度
    )
    
    return ring

def main():
    window_name = 'Triple Eccentric Ring'
    cv2.namedWindow(window_name)
    
    while True:
        # 绘制帧
        frame = draw_frame()
        
        if frame is None:
            print("Error: Invalid circle configuration")
            break
            
        # 显示帧
        cv2.imshow(window_name, frame)
        
        # 检查退出
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 