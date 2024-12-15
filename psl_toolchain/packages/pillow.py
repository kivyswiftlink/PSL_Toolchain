from psl_toolchain.targets import SwiftTarget
from psl_toolchain.package import SwiftPackage

from kivy_ios.toolchain import Recipe
from kivy_ios.recipes.kivy import KivyRecipe

PackageDependency = SwiftTarget.PackageDependency

recipes: list[Recipe] = [
    KivyRecipe()
]


dependencies: list[PackageDependency | str] = [
    PackageDependency("SDL2Core", "SDL2Core"),
    "libSDL2_mixer",
    "libSDL2_ttf",
    "libSDL2_image",
    "libSDL2",
]



class SDL2Core(SwiftPackage):
    
    include_pythoncore = True
    include_pythonswiftlink = True
    
    @property
    def products(self) -> list[SwiftPackage.Product]: 
        return [
            SwiftPackage.Product("SDL2Core", ["SDL2Core"]),
        ]
    
    @property
    def _targets(self) -> list[SwiftTarget]:
        return [
            SwiftTarget(
                "SDL2Core",
                recipes,
                dependencies
            )
        ]
    
    @property
    def dependencies(self) -> list[SwiftPackage.Dependency]:
        return [
            SwiftPackage.Dependency("https://github.com/KivySwiftLink/ImageCore", version=self.version)
        ]



package = SDL2Core()