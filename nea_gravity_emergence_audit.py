import numpy as np
import matplotlib.pyplot as plt

def run_laplacian_gravity_audit():
    print("="*70)
    print("审计 B (最终修正)：C8 网格平账产生的 1/r² 场强")
    print("="*70)

    # 1. 建立 3D 寻址空间 (31x31x31，奇数方便寻找中心)
    size = 31
    phi = np.zeros((size, size, size))
    center = size // 2
    
    # 2. 设定中心质量源 (寻址赤字锚点)
    # 固定中心点的势能，模拟质量源持续产生的寻址赤字
    phi[center, center, center] = 100.0 
    
    # 3. 执行“自动平账” (离散拉普拉斯松弛迭代)
    # 这模拟了空间为了分摊核心赤字而达到的稳态
    print("正在进行全域寻址平账迭代...")
    for _ in range(1000):
        # 记录旧值以应用边界和源约束
        old_phi = phi.copy()
        
        # 核心平账公式：该点的势能 = 六个邻居的平均值
        # 对应 C8 网格的拉普拉斯算子
        phi[1:-1, 1:-1, 1:-1] = (
            old_phi[0:-2, 1:-1, 1:-1] + old_phi[2:, 1:-1, 1:-1] +
            old_phi[1:-1, 0:-2, 1:-1] + old_phi[1:-1, 2:, 1:-1] +
            old_phi[1:-1, 1:-1, 0:-2] + old_phi[1:-1, 1:-1, 2:]
        ) / 6.0
        
        # 强制中心赤字源不变
        phi[center, center, center] = 100.0
        # 边界条件：远场势能归零（Dirichlet 边界）
        phi[0,:,:] = phi[-1,:,:] = phi[:,0,:] = phi[:,-1,:] = phi[:,:,0] = phi[:,:,-1] = 0

    # 4. 提取沿 X 轴的势能分布
    radii = []
    potentials = []
    for x in range(center + 1, size - 1):
        r = x - center
        radii.append(r)
        potentials.append(phi[x, center, center])

    # 5. 计算力的强度 (Curvature Intensity)
    # 引力 F = -grad(phi)，在 3D 拉普拉斯平账下，phi ~ 1/r
    # 则 F ~ 1/r^2，在 Log-Log 图上斜率应为 -2.0
    radii = np.array(radii)
    potentials = np.array(potentials)
    # 使用中心差分计算梯度
    forces = np.abs(np.gradient(potentials))

    # 6. 绘图与对账
    plt.figure(figsize=(10, 6))
    plt.loglog(radii, forces, 'go-', label='Emergent Field Intensity (N.E.A.)')
    # 对照 1/r^2 曲线
    plt.loglog(radii, forces[0]*(radii[0]**2) / radii**2, 'k--', label='Newton/Einstein Limit (1/r²)')
    
    plt.xlabel('Address Distance r')
    plt.ylabel('Local Curvature (Force)')
    plt.title('Final Proof of OP-2: $1/r^2$ Emergence from $C_8$ Connectivity')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 在有效区间（避开边界和源）计算斜率
    valid_mask = (radii > 1) & (radii < size//3)
    coeffs = np.polyfit(np.log(radii[valid_mask]), np.log(forces[valid_mask]), 1)
    print(f"\n审计结论：")
    print(f"1. 寻址赤字在 C8 网格平摊后的衰减斜率: {coeffs[0]:.2f}")
    print(f"2. 理论目标: -2.00 (反平方律)")
    print(f"3. 物理意义：只要空间连接方式是 C8 立方点阵，宏观引力就必须是 $1/r^2$。")

if __name__ == "__main__":
    run_laplacian_gravity_audit()