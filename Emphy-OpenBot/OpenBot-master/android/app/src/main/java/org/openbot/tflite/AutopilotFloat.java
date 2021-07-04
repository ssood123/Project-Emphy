// Created by Matthias Mueller - Intel Intelligent Systems Lab - 2020

package org.openbot.tflite;

import android.app.Activity;
import android.graphics.RectF;
import java.io.IOException;

class AutopilotFloat extends Autopilot {

  /** Additional normalization of the used input. */
  private static final float IMAGE_MEAN = 0.0f;

  private static final float IMAGE_STD = 255.0f;

  /**
   * Initializes a {@code AutopilotFloat}.
   *
   * @param activity
   */
  public AutopilotFloat(Activity activity, Model model, Device device, int numThreads)
      throws IOException {
    super(activity, model, device, numThreads);
  }

  @Override
  public boolean getMaintainAspect() {
    return true;
  }

  @Override
  public RectF getCropRect() {
    return new RectF(0.0f, 240.0f / 720.0f, 0.0f, 0.0f);
  }

  @Override
  protected int getNumBytesPerChannel() {
    return 4; // Float.SIZE / Byte.SIZE;
  }

  @Override
  protected void addPixelValue(int pixelValue) {
    imgData.putFloat((((pixelValue >> 16) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
    imgData.putFloat((((pixelValue >> 8) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
    imgData.putFloat(((pixelValue & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
  }
}
