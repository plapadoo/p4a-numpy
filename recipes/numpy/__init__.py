import os
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.toolchain import warning


class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = '1.14.5'
    url = 'https://pypi.python.org/packages/source/n/numpy/numpy-{version}.zip'
    site_packages_name= 'numpy'

    depends = [('python2', 'python3crystax')]

    recipe_dir = os.path.dirname(os.path.realpath(__file__))

    patches = [os.path.join(recipe_dir, 'patches', 'fix-numpy.patch'),
               os.path.join(recipe_dir, 'patches', 'prevent_libs_check.patch'),
               os.path.join(recipe_dir, 'patches', 'ar.patch'),
               os.path.join(recipe_dir, 'patches', 'lib.patch')
    ]

    def get_recipe_env(self, arch):
        env = super(NumpyRecipe, self).get_recipe_env(arch)

        py_ver =self.ctx.python_recipe.version[0:3]
        py_so = '2.7' if py_ver == '2.7' else py_ver + 'm'
        api_ver = self.ctx.android_api
        platform = 'arm' if 'arm' in arch.arch else arch.arch

        flags = " -L{ctx.ndk_dir}/platforms/android-{api_ver}/arch-{platform}/usr/lib/" \
                " --sysroot={ctx.ndk_dir}/platforms/android-{api_ver}/arch-{platform}" \
            .format(ctx=self.ctx, arch=arch, platform=platform, api_ver=api_ver)

        if {'python3crystax'}:
            flags += " -I{ctx.ndk_dir}/sources/crystax/include/" \
                     " -I{ctx.ndk_dir}/sources/python/{py_ver}/include/python/" \
                     " -L{ctx.ndk_dir}/sources/crystax/libs/{arch.arch}/" \
                     " -L{ctx.ndk_dir}/sources/python/{py_ver}/libs/{arch.arch}/ -lpython{py_so}" \
                .format(ctx=self.ctx, arch=arch, py_so=py_so, py_ver=py_ver)

        if flags not in env['CC']:
            env['CC'] += flags
        if flags not in env['LD']:
            env['LD'] += flags + ' -shared'

        return env

recipe = NumpyRecipe()
