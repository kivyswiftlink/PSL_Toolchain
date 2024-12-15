from os.path import join, dirname, realpath, exists, isdir, basename, splitext
from os import listdir, unlink, makedirs, environ, chdir, getcwd, walk
import sh
import shutil
import json
import importlib
import sys
from context import PackageContext
from targets import BinaryTarget, SwiftTarget
from sh import Command
from typing import Generator
from kivy_ios.toolchain import ensure_dir
import subprocess

def copy_package_content(cls: "SwiftPackage"):
    print(cls.get_binary_targets)

class SwiftPackage:
    
    class Product:
        name: str
        targets: list[str]
        
        def __init__(self, name: str, targets: list[str]):
            self.name = name
            self.targets = targets
        
        @property
        def dump(self) -> dict:
            return {
                "name": self.name,
                "targets": self.targets
            }
    
    class Dependency:
        url: str
        version: str | None
        next_major: str | None
        next_minor: str | None
        
        
        def __init__(self, url: str, version: str | None = None, next_major: str | None = None, next_minor: str | None = None):
            self.url = url
            self.version = version
            self.next_major = next_major
            self.next_minor = next_minor
            
        @property
        def dump(self) -> dict:
            version = self.version
            major = self.next_major
            minor = self.next_minor
            _type = "extact"
            if major:
                _type = "upToNextMajor"
                version = major
            elif minor:
                _type = "upToNextMinor"
                version = minor
            elif not version:
                version = "0.0.0"
            
            return {
                "type": _type,
                #"data": {
                    "url": self.url,
                    "version": version
                #}
            }
            
            
    ctx: PackageContext | None
    products: list[Product]
    dependencies: list[Dependency]
    _targets: list[SwiftTarget]
    version: str = "311.0.0"
    
    include_pythoncore: bool = False
    include_pythonswiftlink: bool = False
    
    def init_with_ctx(self, ctx: PackageContext):
        self.ctx = ctx
        for target in self._targets:
            for recipe in target.recipes:
                recipe.init_with_ctx(ctx)
    
    def execute(self):
        print(self.get_binary_targets)
        self.copy_files_to_package()
        
        with open(join(self.swift_package_dir, "package.json"), "w") as fp:
            json.dump(self.dump, fp)
            
        #spw = shutil.which("SwiftPackageWriter")

        package_string = str(sh.SwiftPackageWriter("create", join(self.swift_package_dir, "package.json")))
        with open(join(self.swift_package_dir, "Package.swift"), "w") as fp:
            fp.write(package_string)
        
        
    def copy_files_to_package(self):
        self.zip_xc_frameworks_to_export()
    
    @property
    def targets(self) -> list[SwiftTarget | BinaryTarget]:
        output: list[SwiftTarget | BinaryTarget] = list(self._targets)
        for src in self.get_binary_targets:
            output.append(
                BinaryTarget(
                    splitext(basename(src))[0],
                    src,
                    "kivyswiftlink",
                    self.__class__.__name__,
                    self.version
                )
            )
        return output
    
    def get_all_xcframeworks(self):
        #xcframeworks: list[str] = []
        
        for target in self._targets:
            for xc in target.xcframeworks:
                yield xc
                #xcframeworks.append(xc)
        #return xcframeworks
    
    @property
    def get_binary_targets(self) -> list[str]:
        bin_targets: list[str] = []
        root = self.swift_package_xcframeworks
        for xc in self.get_all_xcframeworks():
            #root = dirname(xc)
            fn, ext = splitext(basename(xc))
            bin_targets.append(join(root, f"{fn}.zip"))
        
        return bin_targets
    
    @property
    def get_dependencies(self) -> list[Dependency]:
        deps = list(self.dependencies)
        if self.include_pythonswiftlink:
            deps.append(
                SwiftPackage.Dependency("https://github.com/KivySwiftLink/PythonSwiftLink", next_major="311.1.0")
            )
        if self.include_pythoncore:
            deps.append( 
                SwiftPackage.Dependency("https://github.com/KivySwiftLink/PythonCore", next_major="311.0.0")
            )
        return deps
    
    @property
    def swift_package_dir(self) -> str:
        return join(self.ctx.swift_packages, self.__class__.__name__)
    
    @property
    def swift_package_xcframeworks(self) -> str:
        return join(self.swift_package_dir, "xcframeworks")
    
    @property
    def swift_package_site(self) -> str:
        return join(self.swift_package_dir, "site-packages")
    
    @property
    def dump(self) -> dict:
        return {
            "name": self.__class__.__name__,
            "products": [p.dump for p in self.products],
            "dependencies": [dep.dump for dep in self.get_dependencies],
            "targets": [target.dump for target in self.targets],
            "version": self.version
        }
        
    def zip_xc_frameworks_to_export(self):
        last_path = getcwd()
        xc_export_root = self.swift_package_xcframeworks
        ensure_dir(xc_export_root)
        for xc in self.get_all_xcframeworks():
            chdir(dirname(xc))
            xc_basename = basename(xc)
            fn = splitext(xc_basename)[0]
            zip_name = f"{fn}.zip"
            zipfile = join(xc_export_root, f"{fn}.zip")
            Command("/usr/bin/zip")("-r", zipfile, xc_basename)
        chdir(last_path)
        
    
            
        
    @classmethod
    def get_package(cls, name, ctx) -> "SwiftPackage":
        # if not hasattr(cls, "recipes"):
        #     cls.recipes = {}

        if '==' in name:
            name, version = name.split('==')
        else:
            version = None

        mod = importlib.import_module(f"packages.{name}")
        package: SwiftPackage = mod.package
        #recipe.recipe_dir = join(ctx.root_dir, "packages", name)

        #recipe.init_after_import(ctx)

        if version:
            package.version = version

        return package
    
class PythonSwiftPackage(SwiftPackage):
    site_package_targets: list[str]
    
    def copy_files_to_package(self):
        super().copy_files_to_package()
        self.copy_site_package_folder()

    def copy_site_package_folder(self):
        site_packages_dir = self.ctx.site_packages_root
        target_root = self.swift_package_site
        ensure_dir(site_packages_dir)
        for target in self.site_package_targets:
            src = join(site_packages_dir, target)
            if exists(src):
                if isdir(src):
                    shutil.copytree(src, join(target_root, target))
                else:
                    shutil.copy(src, target_root)
                    

    
    @property
    def dump(self) -> dict:
        data = super().dump
        data["site_package_targets"] = self.site_package_targets
        return data

class CythonSwiftPackage(PythonSwiftPackage):
    
    ...
    
    
    

    

        
        
                