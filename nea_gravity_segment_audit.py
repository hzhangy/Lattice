import numpy as np
import matplotlib.pyplot as plt

def run_laplacian_gravity_audit():
    print("="*80)
    print(f"{'N.E.A. OP-2 分段寻址斜率审计报告':^80}")
    print("="*80)

    # 1. 建立 3D 空间 (保持 31 规模以确保在你的 Mac mini 上快速运行)
    size = 31
    phi = np.zeros((size, size, size))
    center = size // 2
    phi[center, center, center] = 100.0 
    
    # 2. 迭代平账
    print("正在进行全域寻址平账迭代 (1000次)...")
    for _ in range(1000):
        old_phi = phi.copy()
        phi[1:-1, 1:-1, 1:-1] = (
            old_phi[0:-2, 1:-1, 1:-1] + old_phi[2:, 1:-1, 1:-1] +
            old_phi[1:-1, 0:-2, 1:-1] + old_phi[1:-1, 2:, 1:-1] +
            old_phi[1:-1, 1:-1, 0:-2] + old_phi[1:-1, 1:-1, 2:]
        ) / 6.0
        phi[center, center, center] = 100.0
        phi[0,:,:] = phi[-1,:,:] = phi[:,0,:] = phi[:,-1,:] = phi[:,:,0] = phi[:,:,-1] = 0

    # 3. 提取数据
    radii = []
    potentials = []
    for x in range(center + 1, size - 1):
        radii.append(x - center)
        potentials.append(phi[x, center, center])

    radii = np.array(radii)
    forces = np.abs(np.gradient(potentials)) # F = -d(phi)/dr
    
    # 4. 计算局部斜率 (Point-to-Point Local Slope)
    # slope = [ln(F2) - ln(F1)] / [ln(r2) - ln(r1)]
    log_r = np.log(radii)
    log_f = np.log(forces)
    local_slopes = np.diff(log_f) / np.diff(log_r)

    print(f"\n{'距离 (r)':<10} | {'场强 (Force)':<15} | {'局部斜率 (Slope)':<15} | {'状态审计'}")
    print("-" * 80)
    
    for i in range(len(local_slopes)):
        r = radii[i]
        f = forces[i]
        s = local_slopes[i]
        
        # 审计逻辑判定
        if i == 0:
            status = "近场启动 (Lattice Rigidity)"
        elif i < 4:
            status = "加速补偿 (Catch-up Phase)"
        elif abs(s + 2.0) < 0.2:
            status = "★ 连续极限区 (Einsteinian)"
        elif i > len(local_slopes) - 4:
            status = "视界压迫 (Boundary Effect)"
        else:
            status = "寻址切换区"
            
        print(f"{r:<10.1f} | {f:<15.6f} | {s:<15.4f} | {status}")

    # 5. 可视化
    plt.figure(figsize=(10, 6))
    plt.loglog(radii, forces, 'go-', label='Emergent Field (NEA)')
    plt.loglog(radii, forces[2]*(radii[2]**2) / radii**2, 'k--', alpha=0.6, label='Ideal 1/r²')
    plt.xlabel('Distance r')
    plt.ylabel('Local Curvature (Force)')
    plt.title('Segmental Audit: The Trajectory of Gravity Emergence')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.show()

if __name__ == "__main__":
    run_laplacian_gravity_audit()