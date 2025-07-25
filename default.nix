with (import <nixpkgs> {});

let env = bundlerEnv {
    name = "kmcconnaughay.github.io";
    inherit ruby;
    gemfile = ./Gemfile;
    lockfile = ./Gemfile.lock;
    gemset = ./gemset.nix;
  };
in stdenv.mkDerivation {
  name = "kmcconnaughay.github.io";
  buildInputs = [env bundler ruby];
}