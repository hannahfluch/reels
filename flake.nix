{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  };

  outputs =
    { nixpkgs, ... }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      libs = with pkgs; [
        stdenv.cc.cc.lib
        zlib
        libxcb
        libGL
        glib
        expat
        nspr
        nss
        atk
        dbus
        libx11
        libxcomposite
        libxdamage
        libxext
        libxfixes
        libxrandr
        libgbm
        libxkbcommon
        alsa-lib

      ];
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShellNoCC {
        buildInputs = [ pkgs.ffmpeg ];
        env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath libs;
      };
    };
}
