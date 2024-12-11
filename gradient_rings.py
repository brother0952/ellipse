import cv2
import numpy as np

def create_ring_gradient(size, center, inner_radius, outer_radius, brightness):
    """创建单个圆环渐变
    
    Args:
        size: (width, height) 画布尺寸
        center: (x, y) 圆心位置
        inner_radius: 内圆半径
        outer_radius: 外圆半径
        brightness: 边界亮度值 (0-1)
    """
    canvas = np.zeros(size, dtype=np.float32)
    y, x = np.ogrid[:size[0], :size[1]]
    
    # 计算到中心点的距离
    dist_from_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    
    # 只在两个圆之间的区域创建渐变
    ring_mask = (dist_from_center >= inner_radius) & (dist_from_center <= outer_radius)
    
    if ring_mask.any():
        # 在每条射线上创建渐变
        gradient = np.zeros_like(dist_from_center)
        valid_points = ring_mask
        
        # 计算从内圆到外圆的线性渐变
        gradient[valid_points] = (dist_from_center[valid_points] - inner_radius) / (outer_radius - inner_radius)
        
        # 在外圆处亮度最大，向内圆渐变到0
        gradient = (1 - gradient) * brightness
        canvas[valid_points] = gradient[valid_points]
    
    return canvas

def draw_frame():
    # 创建黑色画布 (480, 640)
    canvas = np.zeros((480, 640), dtype=np.float32)
    center = (320, 240)  # 画布中心
    
    # 创建圆环 (半径 120-150)
    ring = create_ring_gradient(
        size=(480, 640),
        center=center,
        inner_radius=120,
        outer_radius=150,
        brightness=0.3
    )
    
    return ring

def main():
    window_name = 'Gradient Ring'
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