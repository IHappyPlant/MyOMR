def get_iou(groundtruth_box, predicted_box):
    # compute the intersection over union
    # determine the (x, y)-coordinates of the intersection rectangle
    xa = max(groundtruth_box[0], predicted_box[0])
    ya = max(groundtruth_box[1], predicted_box[1])
    xb = min(groundtruth_box[2], predicted_box[2])
    yb = min(groundtruth_box[3], predicted_box[3])

    # area of intersection rectangle
    inter_area = max(0, xb - xa + 1) * max(0, yb - ya + 1)

    groundtruth_box_area = (groundtruth_box[2] - groundtruth_box[0] + 1) * \
                           (groundtruth_box[3] - groundtruth_box[1] + 1)
    predicted_box_area = (predicted_box[2] - predicted_box[0] + 1) * \
                         (predicted_box[3] - predicted_box[1] + 1)

    return inter_area / float(groundtruth_box_area + predicted_box_area -
                              inter_area)


def build_confusion_matrix(processed_images, groundtruth_images, num_classes):
    length = len(groundtruth_images)
    matrix = [[0 for _ in range(num_classes + 1)] for _ in range(num_classes + 1
                                                                 )]
    for i in range(length):
        processed_img = processed_images[i]
        grundtruth_img = groundtruth_images[i]
        objects_len = len(grundtruth_img['boxes'])
        used_boxes = []
        for j in range(objects_len):
            box = grundtruth_img['boxes'][j]
            class_ = grundtruth_img['classes'][j]
            finded_roi = None
            predicted_class = None
            for k in range(len(processed_img['rois'])):
                roi = processed_img['rois'][k]
                roi = [roi[1], roi[0], roi[3], roi[2]]
                if get_iou(box, roi) > 0.2:
                    finded_roi = roi
                    predicted_class = processed_img['class_ids'][k]
                    used_boxes.append(list(box))
                    break
            if finded_roi:
                matrix[class_][predicted_class] += 1
        if objects_len > len(processed_img['rois']):
            for j in range(objects_len):
                if not list(grundtruth_img['boxes'][j]) in used_boxes:
                    class_ = grundtruth_img['classes'][j]
                    matrix[class_][-1] += 1
    return matrix


def get_model_accuracy(confusion_matrix):
    i = 0
    true = 0
    total = 0
    for row in confusion_matrix:
        true += row[i]
        total += sum(row)
        i += 1
    try:
        return true / total
    except ZeroDivisionError:
        return 1.0


def get_class_precision(confusion_matrix, class_id):
    true = confusion_matrix[class_id][class_id]
    total = sum([row[class_id] for row in confusion_matrix])
    try:
        return true / total
    except ZeroDivisionError:
        return 1.0


def get_class_recall(confusion_matrix, class_id):
    true = confusion_matrix[class_id][class_id]
    total = sum(confusion_matrix[class_id])
    try:
        return true / total
    except ZeroDivisionError:
        return 1.0


def get_class_f1_score(confusion_matrix, class_id, precision=None, recall=None):
    if precision and recall:
        return 2 * precision * recall / (precision + recall)
    prec = get_class_precision(confusion_matrix, class_id)
    rec = get_class_recall(confusion_matrix, class_id)
    return 2 * prec * rec / (prec + rec)


def get_all_scores(confusion_matrix, class_ids):
    accuracy = get_model_accuracy(confusion_matrix)
    precisions = [get_class_precision(confusion_matrix, id_) for id_ in
                  class_ids]
    recalls = [get_class_recall(confusion_matrix, id_) for id_ in class_ids]
    f1_scores = [get_class_f1_score(confusion_matrix, id_) for id_ in class_ids]
    return {
        'accuracy': accuracy,
        'precisions': precisions,
        'recalls': recalls,
        'f1_scores': f1_scores
    }
