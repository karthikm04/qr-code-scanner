import cv2
from pyzbar.pyzbar import decode
import webbrowser

def qr_code_scanner():
    cap = cv2.VideoCapture(0)
    redirected = False  # Flag to track if redirection has occurred

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print("QR Code Detected: ", qr_data)

            # Redirect only if not already redirected and the data is a URL
            if not redirected and (qr_data.startswith("http://") or qr_data.startswith("https://")):
                print(f"Opening link: {qr_data}")
                webbrowser.open(qr_data)
                redirected = True  # Set flag to prevent further redirects

            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

            cv2.putText(frame, qr_data, (points[0].x, points[0].y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the QR code scanner
qr_code_scanner()