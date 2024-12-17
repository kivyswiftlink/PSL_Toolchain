from psl_toolchain.targets import SwiftTarget, TargetDependency
from psl_toolchain.package import SwiftPackage

from kivy_ios.toolchain import Recipe
from kivy_ios.recipes import libjpeg, libpng

PackageDependency = SwiftTarget.PackageDependency


class FreeTypeTarget(SwiftTarget):
    
    name = "freetype"
    
    recipes = [libpng.recipe]


class FreeType(SwiftPackage):
    
    only_include_binary_targets = True
    
    repo_url = "https://github.com/kivyswiftlink/FreeType"
    
    products = [
        SwiftPackage.Product("freetype", ["libfreetype"]),
    ]
    
    targets = [
        FreeTypeTarget()
    ]
    



package = FreeType()