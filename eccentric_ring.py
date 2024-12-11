import cv2
import numpy as np

def create_eccentric_ring_gradient(size, outer_center, outer_radius, inner_center, inner_radius, outer_brightness, inner_brightness):
    """创建偏心圆环渐变
    
    Args:
        size: (width, height) 画布尺寸
        outer_center: (x, y) 外圆圆心位置
        outer_radius: 外圆半径
        inner_center: (x, y) 内圆圆心位置
        inner_radius: 内圆半径
        outer_brightness: 外圆亮度值 (0-1)
        inner_brightness: 内圆亮度值 (0-1)
    """
    canvas = np.zeros(size, dtype=np.float32)
    y, x = np.ogrid[:size[0], :size[1]]
    
    # 计算到外圆圆心的距离
    dist_from_outer = np.sqrt((x - outer_center[0])**2 + (y - outer_center[1])**2)
    
    # 计算到内圆圆心的距离
    dist_from_inner = np.sqrt((x - inner_center[0])**2 + (y - inner_center[1])**2)
    
    # 找出在外圆内但不在内圆内的区域
    ring_mask = (dist_from_outer <= outer_radius) & (dist_from_inner >= inner_radius)
    
    if ring_mask.any():
        gradient = np.zeros_like(dist_from_outer)
        valid_points = ring_mask
        
        # 对于每个点，计算它到内圆边界的最短距离
        dist_to_inner = dist_from_inner - inner_radius
        # 对于每个点，计算它到外圆边界的最短距离
        dist_to_outer = outer_radius - dist_from_outer
        
        # 计算总距离（用于归一化）
        total_dist = dist_to_inner + dist_to_outer
        
        # 在有效区域计算渐变
        ratio = dist_to_inner[valid_points] / total_dist[valid_points]
        
        # 在外圆和内圆之间进行亮度渐变
        gradient[valid_points] = outer_brightness + (inner_brightness - outer_brightness) * ratio
        
        canvas[valid_points] = gradient[valid_points]
    
    return canvas

def draw_frame():
    # 创建黑色画布 (480, 640)
    canvas = np.zeros((480, 640), dtype=np.float32)
    
    # 设置外圆和内圆的参数
    outer_center = (320, 240)  # 外圆圆心在画布中心
    outer_radius = 150
    
    # 内圆圆心偏离外圆圆心
    offset_x, offset_y = 30, 20  # 可以调整这些值来改变内圆位置
    inner_center = (320 + offset_x, 240 + offset_y)
    inner_radius = 100
    
    # 创建偏心圆环
    ring = create_eccentric_ring_gradient(
        size=(480, 640),
        outer_center=outer_center,
        outer_radius=outer_radius,
        inner_center=inner_center,
        inner_radius=inner_radius,
        outer_brightness=0.9,  # 设置外圆亮度
        inner_brightness=0.1   # 设置内圆亮度
    )
    
    return ring

def main():
    window_name = 'Eccentric Ring'
    cv2.namedWindow(window_name)
    
    while True:
        # 绘制帧
        frame = draw_frame()
        
        # 显示帧
        cv2.imshow(window_name, frame)
        
        # 检查退出
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 