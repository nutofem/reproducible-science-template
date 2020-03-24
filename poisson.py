import matplotlib
matplotlib.use("pgf")
import matplotlib.pyplot as plt
plt.rcParams['figure.constrained_layout.use'] = True

from dolfin import *

def poisson_error(N, order=1, plot=False):
    # Create mesh and define function space
    mesh = UnitSquareMesh(N, N)
    V = FunctionSpace(mesh, 'P', order)

    # Define boundary condition
    u_D = Expression('1 + x[0]*x[0] + 2*x[1]*x[1]', degree=6)

    def boundary(x, on_boundary):
        return on_boundary

    bc = DirichletBC(V, u_D, boundary)

    # Define variational problem
    u = TrialFunction(V)
    v = TestFunction(V)
    f = Constant(-6.0)
    a = dot(grad(u), grad(v))*dx
    L = f*v*dx

    # Compute solution
    u = Function(V)
    solve(a == L, u, bc)

    if plot:
        # Save solution to file in VTK format
        vtkfile = File(r'poisson.pvd')
        vtkfile << u

    # Compute error in L2 norm
    error_L2 = errornorm(u_D, u, 'L2')
    return error_L2

if __name__ == "__main__":
    Ns = [1, 2, 4, 8, 16, 32, 64, 128]
    errors = []
    for N in Ns:
        errors.append(poisson_error(N, plot=N==128))
    plt.loglog([1./N for N in Ns], errors, "-kx")
    plt.xlabel("Mesh size $h$")
    plt.ylabel("$L_2$ error norm")
    plt.savefig("poisson_convergence.pdf")

