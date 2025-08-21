#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::WindowEvent;

#[tauri::command]
fn open_dashboard(window: tauri::Window) {
  let _ = window.show();
  let _ = window.unminimize();
  let _ = window.set_focus();
}

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![open_dashboard])
    // v2 signature: (window, event)
    .on_window_event(|window, event| {
      if let WindowEvent::CloseRequested { api, .. } = event {
        let _ = window.hide();
        api.prevent_close();
      }
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
