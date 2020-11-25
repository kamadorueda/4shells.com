let
  sources = import ../../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../../build/utils/ctx)
    // (rec {
      name = "server-build";

      buildInputs = [
        nixpkgs.nodejs
      ];
    })
  )
