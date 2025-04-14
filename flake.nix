{
    description = "Sigma development environment";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    };

    outputs = { nixpkgs, ... }:
    let
        lib = nixpkgs.lib;
        systems = [ "x86_64-linux" ];

        forEachSystem = fn: lib.genAttrs systems (system:
        let
            pkgs = import nixpkgs { inherit system; };
        in fn { inherit pkgs; } );
    in {
        devShells = forEachSystem ({ pkgs }: let
            libs = with pkgs; [
                libxml2
                libxslt
            ];
            tools = with pkgs; [
                podman
                podman-compose
                uv
            ];
        in {
            default = pkgs.mkShell {
                name = "sigma";

                buildInputs = libs;
                packages = tools;

                # This makes sure python libraries can find the TLS root certificate
                shellHook = ''
                    export SSL_CERT_FILE="$(uv run python3 -m certifi)"
                '';

                LD_LIBRARY_PATH = lib.makeLibraryPath libs;
            };
        });
    };
}
