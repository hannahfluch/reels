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
        libz
      ];
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShellNoCC {
        env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath libs;
      };
    };
}
