import numpy as np
import cv2


def _resize_and_fill_gaps(matrix, scale, label_height):
    # height and width of the first image
    height, width, *_ = matrix[0][0].shape
    height = int(height * scale)
    width = int(width * scale)

    n_rows = len(matrix)
    n_cols = 0

    for row in matrix:
        if len(row) > n_cols:
            n_cols = len(row)

    result = np.zeros(
        (n_rows, n_cols, height+label_height, width, 3), dtype=np.uint8)

    for r_idx, row in enumerate(matrix):
        for c_idx, img in enumerate(row):
            img = np.squeeze(img)
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            img = cv2.resize(img, (width, height))
            text_place = np.zeros((label_height, width, 3))

            result[r_idx, c_idx] = np.vstack((img, text_place))

    return result


def stackIt(img_matrix, label_matrix=None,  img_scale=1, label_height=30, **kwargs):
    label_height = 0 if label_matrix == None else label_height
    img_matrix = _resize_and_fill_gaps(img_matrix, img_scale, label_height)

    # putting the labels in each images
    if label_matrix:
        for img_row, label_row in zip(img_matrix, label_matrix):
            for image, label in zip(img_row, label_row):
                h, *_ = image.shape
                cv2.putText(image, label, (10, h-10), **kwargs)

    row_images = []
    for row in img_matrix:
        row_images.append(np.hstack(tuple([*row])))

    return np.vstack(tuple([*row_images]))


def draw_border(
    img, x1, y1, x2, y2, score, line_thickness=1, line_color=(255, 255, 255), r=0, d=30,
    edge_color=(100, 46, 21), edge_thickness=5, draw_line=False
):

    # Top left
    cv2.line(
        img, (x1 + r, y1), (x1 + r + d, y1), edge_color, edge_thickness
    )
    cv2.line(
        img, (x1, y1 + r), (x1, y1 + r + d), edge_color, edge_thickness
    )
    cv2.ellipse(
        img, (x1 + r, y1 + r), (r, r), 180, 0, 90, edge_color, edge_thickness
    )

    # Top right
    cv2.line(
        img, (x2 - r, y1), (x2 - r - d, y1), edge_color, edge_thickness
    )
    cv2.line(
        img, (x2, y1 + r), (x2, y1 + r + d), edge_color, edge_thickness
    )
    cv2.ellipse(
        img, (x2 - r, y1 + r), (r, r), 270, 0, 90, edge_color, edge_thickness
    )

    # Bottom left
    cv2.line(
        img, (x1 + r, y2), (x1 + r + d, y2), edge_color, edge_thickness
    )
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d),
             edge_color, edge_thickness)
    cv2.ellipse(
        img, (x1 + r, y2 - r), (r, r), 90, 0, 90, edge_color, edge_thickness
    )

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2),
             edge_color, edge_thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d),
             edge_color, edge_thickness)
    cv2.ellipse(
        img, (x2 - r, y2 - r), (r, r), 0, 0, 90, edge_color, edge_thickness
    )

    if draw_line:
        # top line
        cv2.line(img, (x1+r+d, y1), (x2-r-d, y1),
                 line_color, line_thickness)

        # left line
        cv2.line(img, (x1, y1+r+d), (x1, y2-r-d),
                 line_color, line_thickness)

        # right line
        cv2.line(img, (x2, y1+r+d), (x2, y2-r-d),
                 line_color, line_thickness)

        # bottom line
        cv2.line(img, (x1+r+d, y2), (x2-r-d, y2),
                 line_color, line_thickness)

    # put score
    if score != None:
        cv2.rectangle(
            img, (x1, y1-40), (x1+140, y1-6), (100, 46, 21), cv2.FILLED
        )
        cv2.putText(
            img, f'Score: {score:.2f}', (x1+7,
                                         y1-15), cv2.FONT_HERSHEY_SIMPLEX,
            .7, (255, 255, 255), 1
        )
    return x1, y1, x2, y2
