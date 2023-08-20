# Conven hull problem
# Input: random points
# Output: convex hull of the points, represented by the sequence of points in the boundary in clockwise order


from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np

NUM_POINTS = 10

def convex_hull(points):
    # sort the points by x-coordinate
    points = points[points[:, 0].argsort()]
    return convex_hull_recursion(points)

def convex_hull_recursion(points):
    n = len(points)
    if n <= 2:
        return points
    else:
        return merge(convex_hull_recursion(points[:n//2, :]), convex_hull_recursion(points[n//2:, :]))
        
def merge(a, b):
    # a and b are boundary points of the convex hull, given in clockwise order
    na = len(a)
    nb = len(b)
    a1_idx = 0
    b1_idx = 0

    # find the rightmost point of a
    for i in range(na):
        if a[i, 0] > a[a1_idx, 0]:
            a1_idx = i

    # find the leftmost point of b
    for i in range(nb):
        if b[i, 0] < b[b1_idx, 0]:
            b1_idx = i

    L = (a[a1_idx, 0] + b[b1_idx, 0]) / 2
    # find the upper tangent
    ah_idx = a1_idx
    bh_idx = b1_idx
    while True:
        if get_y(L, a[(ah_idx-1)%na], b[bh_idx]) > get_y(L, a[ah_idx], b[bh_idx]):  
            ah_idx = (ah_idx - 1) % na
        elif get_y(L, a[ah_idx], b[(bh_idx+1)%nb]) > get_y(L, a[ah_idx], b[bh_idx]):
            bh_idx = (bh_idx + 1) % nb
        else:
            break

    # find the lower tangent
    al_idx = a1_idx
    bl_idx = b1_idx
    while True:
        if get_y(L, a[(al_idx+1)%na], b[bl_idx]) < get_y(L, a[al_idx], b[bl_idx]):
            al_idx = (al_idx + 1) % na
        elif get_y(L, a[al_idx], b[(bl_idx-1)%nb]) < get_y(L, a[al_idx], b[bl_idx]):
            bl_idx = (bl_idx - 1) % nb
        else:
            break

    ret = []
    a_idx = al_idx
    b_idx = bh_idx
    while True:
        ret.append(a[a_idx])
        if a_idx == ah_idx:
            break
        a_idx = (a_idx + 1) % na
    while True:
        ret.append(b[b_idx])
        if b_idx == bl_idx:
            break
        b_idx = (b_idx + 1) % nb
    return np.array(ret)
        
    
# return y-coordinate of intersection of L and segment (a, b)    
def get_y(L, a, b):
    return (a[1] - b[1]) / (a[0] - b[0]) * (L - a[0]) + a[1]

if __name__ == "__main__":
    # generate random points in 2-D such that all have different x and y coordinates
    points = np.random.choice(range(NUM_POINTS*2), (NUM_POINTS, 2), replace=False)

    my_hull = convex_hull(points)
    hull = ConvexHull(points)

    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(10, 3))

    for ax in (ax1, ax2, ax3):
        ax.plot(points[:, 0], points[:, 1], '.', color='k')
        if ax == ax1:
            ax.set_title('Given points')
        elif ax == ax2:
            ax.set_title('Convex hull')
            for simplex in hull.simplices:
                ax.plot(points[simplex, 0], points[simplex, 1], 'c')
            ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'o', mec='r', color='none', lw=1, markersize=10)
        else:
            ax.set_title('My hull')
            ax.plot(my_hull[:, 0], my_hull[:, 1], 'o', mec='r', color='none', lw=1, markersize=10)
            for i in range(len(my_hull)):
                ax.plot([my_hull[i, 0], my_hull[(i+1)%len(my_hull), 0]], [my_hull[i, 1], my_hull[(i+1)%len(my_hull), 1]], 'b')
        ax.set_xticks(range(NUM_POINTS*2))
        ax.set_yticks(range(NUM_POINTS*2))
    plt.show()

