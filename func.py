import numpy as np
import csv





def point_distance(A, B):

    if type(A) != np.ndarray:
        A = np.array(A)
    if type(B) != np.ndarray:
        B = np.array(B)
    d = A - B
    d_lat = d[:, 0]
    d_lon = d[:, 1]
    if len(A.shape) == 1:
        lat1 = A[0]
    else:
        lat1 = A[:, 0]
    lat2 = B[:, 0]
    temp = np.sqrt(((d_lat)*111000)**2+((d_lon)*70000)**2)

    return temp

def point_distance2(A, B):
    #print('start')
    #print('probe', type(probe))
    #print('linkp',link_points)
    if type(A) != np.ndarray:
        A = np.array(A)
    if type(B) != np.ndarray:
        B = np.array(B)
    #print(A,B)
    Arad = np.deg2rad(A)
    Brad = np.deg2rad(B)
    #print(Arad,Brad)
    d = Arad - Brad
    d_lat = d[:, 0]
    d_lon = d[:, 1]
    if len(Arad.shape) == 1:
        lat1 = Arad[0]
    else:
        lat1 = Arad[:, 0]
    lat2 = Brad[:, 0]
    temp = np.sin(d_lat/2.0)**2 + np.cos(lat1) * \
        np.cos(lat2) * np.sin(d_lon/2.0)**2
    dis = 12742008 * np.arcsin(np.sqrt(temp))

    return dis


def point_to_line_dis(base, left, right):
    if type(base) != np.ndarray:
        base = np.array(base)
    if type(left) != np.ndarray:
        left = np.array(left)
    if type(right) != np.ndarray:
        right = np.array(right)
    left2 = left ** 2
    right2 = right ** 2
    base2 = base ** 2
    ret = np.zeros_like(base, dtype=np.float)
    mask = np.ones_like(base, dtype=np.bool)
    temp = np.logical_and(base == left+right, mask)
    mask = np.logical_xor(mask, temp)
    ret[temp] = 0
    temp = np.logical_and(base < 1e-10, mask)
    mask = np.logical_xor(mask, temp)
    ret[temp] = left[temp]
    temp = np.logical_and(left2 > base2 + right2, mask)
    mask = np.logical_xor(mask, temp)
    ret[temp] = right[temp]
    temp = np.logical_and(right2 > base2 + left2, mask)
    mask = np.logical_xor(mask, temp)
    ret[temp] = left[temp]

    perimeter = (base[mask] + left[mask] + right[mask]) * 0.5
    area = np.sqrt(perimeter * (perimeter - left[mask]) * (perimeter - right[mask]) * (perimeter - base[mask]))
    ret[mask] = 2 * area / base[mask]
 
    return ret


def distance_r_n(probepoints,linkpoints):
    out=[]
    probepoints = np.array(probepoints)
    linkpoints = np.array(linkpoints)
    base = point_distance(linkpoints[:-1,:],linkpoints[1:,:])
    edge = point_distance(probepoints,linkpoints)
    edge1 = edge[:-1]
    edge2 = edge[1:]
    #print('bee',base,edge1,edge2)
    link_dis = point_to_line_dis(base,edge1,edge2)
    #print('dis',link_dis)
    min_idx = np.argmin(link_dis)
    #print(min_idx)
    ls = (base[min_idx] ** 2 + edge1[min_idx] ** 2  - edge2[min_idx] ** 2) / (2 * base[min_idx])
    #print(ls,type(ls))
    ls1 = np.maximum(ls,0)
    ls2 = np.minimum(ls1,base[min_idx])
    refDistance = np.sum(base[:min_idx]) + ls2
    linksDistance = link_dis[min_idx]
    out.append([refDistance, linksDistance])
    #print(out)
    return out

def distance_pl(probepoints,linkpoints):
    probepoints = np.array(probepoints)
    linkpoints = np.array(linkpoints)
    base = point_distance(linkpoints[:-1,:],linkpoints[1:,:])
    edge = point_distance(probepoints,linkpoints)
    edge1 = edge[:-1]
    edge2 = edge[1:]
    #print('bee',base,edge1,edge2)
    link_dis = point_to_line_dis(base,edge1,edge2)
    link_dis =np.min(link_dis)
    min_idx = np.argmin(link_dis)


    return link_dis,min_idx






















    
