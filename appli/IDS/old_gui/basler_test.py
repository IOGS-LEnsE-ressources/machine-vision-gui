from pypylon import pylon
import cv2
import numpy as np

# Initialiser et ouvrir la caméra
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Configurer la caméra pour utiliser le format BayerRG8
nodemap = camera.GetNodeMap()
pixel_format = nodemap.GetNode("PixelFormat")

if pixel_format:
    pixel_format.SetValue("BayerRG8")  # Configurer le mode BayerRG8
    print("Pixel format configuré sur BayerRG8")
else:
    print("Impossible de configurer le format PixelFormat.")

if camera.IsOpen():
    print("Change FPS")
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(10.0)

# Démarrer l'acquisition
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

try:
    # Capturer une seule image
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        print("Image capturée avec succès")

        # Accéder aux données de l'image brute (BayerRG8)
        bayer_image = grab_result.Array

        # Convertir BayerRG8 en image couleur RGB avec OpenCV
        rgb_image = cv2.cvtColor(bayer_image, cv2.COLOR_BAYER_RG2RGB)

        # Afficher l'image
        cv2.imshow("Image RGB", rgb_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Optionnel : sauvegarder l'image
        cv2.imwrite("image_rgb.png", rgb_image)
    else:
        print(f"Erreur lors de la capture : {grab_result.ErrorDescription}")

    grab_result.Release()

finally:
    # Nettoyage
    camera.StopGrabbing()
    camera.Close()
