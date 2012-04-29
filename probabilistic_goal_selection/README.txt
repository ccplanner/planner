An experiment using Probabilistic Soft Logic to predict goals in Chip's Challenge.

1. Install PSL 1.0.3, i.e. it must be installed in your local Maven repository.

2. mvn clean compile

3. mvn dependency:build-classpath -Dmdep.outputFile=classpath.out

4. java -cp ./target/classes:`cat classpath.out` edu.umd.cs.chipschallenge.CC

As currently written, it tests the following board:

P _ E
_ _ _
_ _ M

Where the locations are numbered as follows:

1 2 3
4 5 6
7 8 9

And the result should be the following, indicating that the selected goal is in position 3, which is the exit.

Model:
{constraint} DataCertainty
{constraint} Functional on goal(Entity, Entity)
{1.0E-6} ttrue(A, B) => goal(A, B)
{1.0} ( ( player(B, P) ^ exit(B, E) ) ^ near(P, E) ) => goal(B, E)
{1.0} ( ( ( player(B, P) ^ monster(B, M) ) ^ near(P, M) ) ^ far(M, G) ) => goal(B, G)
--- Atoms:
goal(100, 3) V=[1]
# Atoms: 1

