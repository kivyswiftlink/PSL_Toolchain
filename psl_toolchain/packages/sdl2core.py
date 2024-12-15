from targets import SwiftTarget
from package import SwiftPackage

from kivy_ios.toolchain import Recipe
from kivy_ios.recipes import sdl2, sdl2_image, sdl2_mixer, sdl2_ttf

PackageDependency = SwiftTarget.PackageDependency

class SDL2CoreTarget(SwiftTarget):
    
    name = "SDL2Core"
    
    recipes = [
        sdl2.recipe,
        sdl2_image.recipe,
        sdl2_mixer.recipe,
        sdl2_ttf.recipe
    ]
    
    dependencies = [
        PackageDependency("libpng", "ImageCore"),
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
            SDL2CoreTarget()
        ]
    
    @property
    def dependencies(self) -> list[SwiftPackage.Dependency]:
        return [
            SwiftPackage.Dependency("https://github.com/KivySwiftLink/ImageCore", version=self.version)
        ]



package = SDL2Core()