{
  description = "swwwcycle";

  inputs = {
    # Pinned to a commit with guaranteed cache
    nixpkgs.url = "github:NixOS/nixpkgs/057f9aecfb71c4437d2b27d3323df7f93c010b7e";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python-env = pkgs.python311.withPackages (ps: [ ps.pyside6 ]);
    in
    {
      packages.${system}.default = pkgs.writeShellScriptBin "swwwcycle" ''
        export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt6.qtbase}/lib/qt-6/plugins"
        exec ${python-env}/bin/python3 ${./main.py} "$@"
      '';

      devShells.${system}.default = pkgs.mkShell {
        packages = [ python-env ];
        
        shellHook = ''
          export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt6.qtbase}/lib/qt-6/plugins"
          echo "✅ Ready! Run: python main.py"
        '';
      };
    };
}