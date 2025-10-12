{
  description = "Python Qt development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python311.withPackages (
          ps: with ps; [
            pyside6
            pyinstaller
          ]
        );
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.qt6.qtbase
            pkgs.qt6.qtdeclarative
            pkgs.qt6.qtwayland
          ];

          shellHook = ''
            export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt6.qtbase.out}/lib/qt-6/plugins"
            echo "Python Qt6 (PySide6) development environment loaded"
          '';
        };
      }
    );
}
