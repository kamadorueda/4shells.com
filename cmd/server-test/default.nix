let
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };
  bin = import ../../build/bin;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "server-test";

      buildInputs = bin.dependencies.fourShellsServerBack ++ [
        nixpkgs.python38Packages.pytest
        nixpkgs.python38Packages.pytestcov
      ];

      srcBack = ../../back;
    })
  )