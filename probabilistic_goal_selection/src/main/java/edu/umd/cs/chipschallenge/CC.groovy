package edu.umd.cs.chipschallenge;

import static org.junit.Assert.*

import org.junit.Test
import org.junit.Before

import edu.umd.cs.psl.config.*
import edu.umd.cs.psl.database.DataStore
import edu.umd.cs.psl.database.DatabaseAtomStoreQuery
import edu.umd.cs.psl.database.RDBMS.DatabaseDriver
import edu.umd.cs.psl.database.RDBMS.RDBMSUniqueIntID
import edu.umd.cs.psl.groovy.PSLModel
import edu.umd.cs.psl.groovy.RelationalDataStore
import edu.umd.cs.psl.model.argument.GroundTerm
import edu.umd.cs.psl.model.atom.memory.SimpleMemoryAtom
import edu.umd.cs.psl.model.function.AttributeSimilarityFunction
import edu.umd.cs.psl.ui.functions.textsimilarity.LevenshteinStringSimilarity
import edu.umd.cs.psl.groovy.*
import edu.umd.cs.psl.model.predicate.type.*

PSLModel m
DataStore data

m = new PSLModel(this);

m.add predicate: "player" , board: Entity, loc: Entity, type: PredicateTypes.BooleanTruth;
m.add predicate: "exit" , board: Entity, loc: Entity, type: PredicateTypes.BooleanTruth;
m.add predicate: "monster" , board: Entity, loc: Entity, type: PredicateTypes.BooleanTruth;
m.add predicate: "goal" , board: Entity, loc: Entity, open: true, type: PredicateTypes.SoftTruth;
m.add predicate: "near" , board: Entity, loc: Entity, type: PredicateTypes.SoftTruth;
m.add predicate: "far" , board: Entity, loc: Entity, type: PredicateTypes.SoftTruth;
m.add predicate: "ttrue", board : Entity, loc: Entity;

data = new RelationalDataStore(m)
data.setup db : DatabaseDriver.H2

m.add PredicateConstraint.Functional , on : goal;

//m.add Prior.Simple, on : goal, weight: 1E-10;

m.add rule : (player(B,P) & exit(B,E) & near(P,E)) >> goal(B,E), weight : 1 ;
m.add rule : (player(B,P) & monster(B,M) & near(P,M) & far(M,G)) >> goal(B,G), weight : 1 ;

m.add rule : ttrue(A,B) >> goal(A,B), weight : 1e-6;

TestingUtil.loadFromString("""
        100	1
        """
        , data.getInserter(player))

TestingUtil.loadFromString("""
        100	3
        """
        , data.getInserter(exit))

TestingUtil.loadFromString("""
        100	9
        """
        , data.getInserter(monster))

def coords = []
for (row in 1..3) {
    for (col in 1..3) {
        coords << [row,col]
    }
}

def sbFar = new StringBuilder()
def sbNear = new StringBuilder()
for (loc1 in 0..7){
    for (loc2 in (loc1+1)..8){
        def disty = (coords[loc2][0] - coords[loc1][0]).abs()
        def distx = (coords[loc2][1] - coords[loc1][1]).abs()
        def dist = distx + disty
        def far = dist / 4.0
        def near = 1-far
        sbFar.append("${loc1+1}\t${loc2+1}\t${far}\n")
        sbFar.append("${loc2+1}\t${loc1+1}\t${far}\n")
        sbNear.append("${loc1+1}\t${loc2+1}\t${near}\n")
        sbNear.append("${loc2+1}\t${loc1+1}\t${near}\n")
    }
}

TestingUtil.loadFromStringWithTruth(sbFar.toString(), data.getInserter(far))
TestingUtil.loadFromStringWithTruth(sbNear.toString(), data.getInserter(near))

def sbGoals = new StringBuilder()
for (loc in 1..9) {
    sbGoals.append("100\t${loc}\t1.0\n")
}
TestingUtil.loadFromStringWithTruth(sbGoals.toString(), data.getInserter(ttrue))

println m

ConfigManager cm = ConfigManager.getManager();
ConfigBundle cb = cm.getBundle("example");
def result = m.mapInference(data.getDatabase(),cb)

result.printAtoms(goal)
