package org.openbot.env;

import android.content.Context;
import android.view.SurfaceView;
import android.view.TextureView;

public interface IVideoServer {
  void startServer();

  void stopServer();

  void setConnected(boolean connected);

  void init(Context context);

  boolean isRunning();

  void startClient();

  void sendServerUrl();

  void sendVideoStoppedStatus();

  void setView(SurfaceView view);

  void setView(TextureView view);

  void setView(com.pedro.rtplibrary.view.OpenGlView view);
}
