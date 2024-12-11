import cv2
import numpy as np

def create_asymmetric_ellipse_gradient(
    size,
    centers,
    axes_left_right,
    brightnesses
):
    """创建五重不对称椭圆渐变"""
    canvas = np.zeros(size, dtype=np.float32)
    
    # 创建坐标网格
    y, x = np.mgrid[:size[0], :size[1]]  # 使用mgrid替代ogrid
    
    # 计算到五个椭圆中心的归一化距离
    distances = []
    for (cx, cy), (left_a, right_a, b) in zip(centers, axes_left_right):
        # 分别计算左右两侧的距离
        dx = x - cx
        dy = y - cy
        
        # 创建距离数组
        dist = np.zeros_like(x, dtype=np.float32)
        
        # 分别处理左右两侧
        left_mask = dx <= 0
        right_mask = dx > 0
        
        # 左半椭圆
        dist[left_mask] = np.sqrt(
            (dx[left_mask] / left_a) ** 2 + 
            (dy[left_mask] / b) ** 2
        )
        
        # 右半椭圆
        dist[right_mask] = np.sqrt(
            (dx[right_mask] / right_a) ** 2 + 
            (dy[right_mask] / b) ** 2
        )
        
        distances.append(dist)
    
    distances = np.array(distances)
    
    # 定义有效区域
    valid_mask = (distances[0] <= 1) & (distances[-1] >= 1)
    
    if valid_mask.any():
        gradient = np.zeros_like(canvas)
        
        # 计算到各个椭圆边界的距离
        dists_to_boundary = []
        for i, dist in enumerate(distances):
            if i == 0:  # 最外椭圆
                d = 1 - dist
            else:  # 其他椭圆
                d = np.abs(1 - dist)
            dists_to_boundary.append(d)
        
        # 计算总距离
        total_dist = sum(dists_to_boundary)
        
        # 在有效区域计算渐变
        if valid_mask.any():
            # 计算每个椭圆的权重
            weights = []
            for d in dists_to_boundary:
                w = np.zeros_like(canvas)
                w[valid_mask] = d[valid_mask] / total_dist[valid_mask]
                weights.append(w)
            
            # 使用权重进行亮度插值
            for w, b in zip(weights, brightnesses):
                gradient += w * b
        
        canvas[valid_mask] = gradient[valid_mask]
    
    return canvas

def draw_frame():
    # 创建黑色画布 (480, 640)
    canvas = np.zeros((480, 640), dtype=np.float32)
    
    # 基准中心点
    base_center = (320, 240)
    
    # 设置五个椭圆的参数
    centers = [
        base_center,                    # 最外椭圆在中心
        (base_center[0]+10, base_center[1]+10),  # 第二椭圆略微偏移
        (base_center[0]+15, base_center[1]+15),  # 第三椭圆继续偏移
        (base_center[0]+20, base_center[1]+20),  # 第四椭圆继续偏移
        (base_center[0]+25, base_center[1]+25),  # 最内椭圆偏移最多
    ]
    
    # 设置椭圆的轴长 (left_a, right_a, b)
    axes_left_right = [
        (180, 120, 120),  # 最外椭圆
        (150, 100, 100),  # 第二椭圆
        (120, 80, 75),    # 第三椭圆
        (90, 60, 50),     # 第四椭圆
        (60, 40, 25),     # 最内椭圆
    ]
    
    # 设置亮度值（从外到内）
    brightnesses = [0.9, 0.7, 0.5, 0.3, 0.1]
    
    # 创建五重不对称椭圆
    ring = create_asymmetric_ellipse_gradient(
        size=(480, 640),
        centers=centers,
        axes_left_right=axes_left_right,
        brightnesses=brightnesses
    )
    
    return ring

def main():
    window_name = 'Quintuple Asymmetric Ellipses'
    cv2.namedWindow(window_name)
    
    while True:
        frame = draw_frame()
        cv2.imshow(window_name, frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 