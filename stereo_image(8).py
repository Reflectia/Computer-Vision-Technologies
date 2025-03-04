from __future__ import print_function
import numpy as np
import cv2
import open3d as o3d

# Define the PLY file header
ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def capture_frames(cap, num_frames=3):
    frames = []
    while len(frames) < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Capture Frames', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            frames.append(frame)
            print(f"Captured frame {len(frames)}")
    cv2.destroyWindow('Capture Frames')
    return frames


def compute_disparity(imgL, imgR, window_size=3, min_disp=16, num_disp=128):
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp - min_disp,
        blockSize=13,
        P1=8 * 7 * window_size**2,
        P2=32 * 7 * window_size**2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )
    disparity = stereo.compute(cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY),
                               cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)).astype(np.float32) / 16.0
    return disparity


def merge_disparity_maps(disp1, disp2):
    # Simple averaging for merging disparity maps
    combined_disp = (disp1 + disp2) / 2
    return combined_disp


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Press 'c' to capture frames.")
    frames = capture_frames(cap)
    cap.release()

    if len(frames) < 3:
        print("Error: Not enough frames captured.")
        return

    img1, img2, img3 = frames[0], frames[1], frames[2]

    print('Computing disparities...')
    disp1 = compute_disparity(img1, img2)
    disp2 = compute_disparity(img1, img3)

    print('Merging disparity maps...')
    disp_combined = merge_disparity_maps(disp1, disp2)

    print('Generating 3D point cloud...')
    h, w = img1.shape[:2]
    f = 0.8 * w  # Focal length guess
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],  # Turn points 180 deg around x-axis
                    [0, 0, 0, -f],  # so that y-axis looks up
                    [0, 0, 1, 0]])
    points = cv2.reprojectImageTo3D(disp_combined, Q)
    colors = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    mask = disp_combined > disp_combined.min()

    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = 'out.ply'
    write_ply(out_fn, out_points, out_colors)
    print(f'{out_fn} saved')

    cv2.imshow('First Image', img1)
    cv2.imshow('Disparity', (disp_combined - disp_combined.min()) / disp_combined.max())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Load and display point cloud
    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud(out_fn)
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd], width=800, height=800, left=50, top=50)


if __name__ == '__main__':
    main()
