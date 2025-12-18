{
  description = "swwwcycle";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/057f9aecfb71c4437d2b27d3323df7f93c010b7e";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      python-env = pkgs.python311.withPackages (ps: [
        ps.pyside6
      ]);

      qtPlugins = pkgs.lib.makeSearchPath "lib/qt-6/plugins" [
        pkgs.qt6.qtbase
        pkgs.qt6.qtwayland
      ];
    in
    {
      packages.${system}.default = pkgs.writeShellScriptBin "swwwcycle" ''
        export QT_QPA_PLATFORM=wayland
        export QT_PLUGIN_PATH="${qtPlugins}"
        exec ${python-env}/bin/python3 ${./main.py} "$@"
      '';

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          python-env
          pkgs.qt6.qtwayland
          pkgs.libglvnd
          pkgs.mesa
          pkgs.snixembed
        ];
      };
    };
}
