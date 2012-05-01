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
        101	1
        102	1
        103	1
        104	1
        105	1
        106	1
        107	2
        108	2
        109	2
        110	2
        111	2
        112	2
        113	2
        114	1
        115	1
        116	1
        117	1
        118	1
        119	1
        120	1
        121	2
        122	2
        123	2
        124	2
        125	2
        126	2
        127	2
        128	1
        129	1
        130	1
        131	1
        132	1
        133	1
        134	1
        135	2
        136	2
        137	2
        138	2
        139	2
        140	2
        141	2
        142	5
        143	5
        144	5
        145	5
        146	5
        147	5
        148	5
        149	5
        150	1
        151	1
        152	1
        153	1
        154	2
        155	2
        156	2
        157	2
        158	1
        159	1
        160	1
        161	1
        162	2
        163	2
        164	2
        165	2
        //100	1
        //101	1
        //102	1
        //103	1
        //104	1
        //105	1
        //106	1
        //107	2
        //108	2
        //109	2
        //110	2
        //111	2
        //112	2
        //113	2
        //114	1
        //115	1
        //116	1
        //117	1
        //118	1
        //119	1
        //120	1
        //121	2
        //122	2
        //123	2
        //124	2
        //125	2
        //126	2
        //127	2
        //128	1
        //129	1
        //130	1
        //131	1
        //132	1
        //133	1
        //134	1
        //135	2
        //136	2
        //137	2
        //138	2
        //139	2
        //140	2
        //141	2
        //142	5
        //143	5
        //144	5
        //145	5
        //146	5
        //147	5
        //148	5
        //149	5
        //150	1
        //151	1
        //152	1
        //153	1
        //154	2
        //155	2
        //156	2
        //157	2
        //158	1
        //159	1
        //160	1
        //161	1
        //162	2
        //163	2
        //164	2
        //165	2
        """
        , data.getInserter(player))

TestingUtil.loadFromString("""
        100	2
        101	2
        102	2
        103	2
        104	2
        105	2
        106	2
        107	1
        108	1
        109	1
        110	1
        111	1
        112	1
        113	1
        114	3
        115	3
        116	3
        117	3
        118	3
        119	3
        120	3
        121	4
        122	4
        123	4
        124	4
        125	4
        126	4
        127	4
        128	6
        129	6
        130	6
        131	6
        132	6
        133	6
        134	6
        135	7
        136	7
        137	7
        138	7
        139	7
        140	7
        141	7
        142	1
        143	1
        144	1
        145	1
        146	2
        147	2
        148	2
        149	2
        150	5
        151	5
        152	5
        153	5
        154	5
        155	5
        156	5
        157	5
        158	9
        159	9
        160	9
        161	9
        162	8
        163	8
        164	8
        165	8
        //100	2
        //101	2
        //102	2
        //103	2
        //104	2
        //105	2
        //106	2
        //107	1
        //108	1
        //109	1
        //110	1
        //111	1
        //112	1
        //113	1
        //114	3
        //115	3
        //116	3
        //117	3
        //118	3
        //119	3
        //120	3
        //121	4
        //122	4
        //123	4
        //124	4
        //125	4
        //126	4
        //127	4
        //128	6
        //129	6
        //130	6
        //131	6
        //132	6
        //133	6
        //134	6
        //135	7
        //136	7
        //137	7
        //138	7
        //139	7
        //140	7
        //141	7
        //142	1
        //143	1
        //144	1
        //145	1
        //146	2
        //147	2
        //148	2
        //149	2
        //150	5
        //151	5
        //152	5
        //153	5
        //154	5
        //155	5
        //156	5
        //157	5
        //158	9
        //159	9
        //160	9
        //161	9
        //162	8
        //163	8
        //164	8
        //165	8
        """
        , data.getInserter(exit))

TestingUtil.loadFromString("""
        100	3
        101	4
        102	5
        103	6
        104	7
        105	8
        106	9
        107	3
        108	4
        109	5
        110	6
        111	7
        112	8
        113	9
        114	2
        115	4
        116	5
        117	6
        118	7
        119	8
        120	9
        121	1
        122	3
        123	5
        124	6
        125	7
        126	8
        127	9
        128	2
        129	3
        130	4
        131	5
        132	7
        133	8
        134	9
        135	1
        136	3
        137	4
        138	5
        139	6
        140	8
        141	9
        142	2
        143	3
        144	6
        145	9
        146	1
        147	4
        148	7
        149	8
        150	2
        151	3
        152	6
        153	9
        154	1
        155	4
        156	7
        157	8
        158	2
        159	3
        160	5
        161	6
        162	1
        163	4
        164	5
        165	7
        //100	3
        //101	4
        //102	5
        //103	6
        //104	7
        //105	8
        //106	9
        //107	3
        //108	4
        //109	5
        //110	6
        //111	7
        //112	8
        //113	9
        //114	2
        //115	4
        //116	5
        //117	6
        //118	7
        //119	8
        //120	9
        //121	1
        //122	3
        //123	5
        //124	6
        //125	7
        //126	8
        //127	9
        //128	2
        //129	3
        //130	4
        //131	5
        //132	7
        //133	8
        //134	9
        //135	1
        //136	3
        //137	4
        //138	5
        //139	6
        //140	8
        //141	9
        //142	2
        //143	3
        //144	6
        //145	9
        //146	1
        //147	4
        //148	7
        //149	8
        //150	2
        //151	3
        //152	6
        //153	9
        //154	1
        //155	4
        //156	7
        //157	8
        //158	2
        //159	3
        //160	5
        //161	6
        //162	1
        //163	4
        //164	5
        //165	7
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
for (board in 100..165) {
//for (board in 100..101) {
    for (loc in 1..9) {
        sbGoals.append("${board}\t${loc}\t1.0\n")
    }
}
TestingUtil.loadFromStringWithTruth(sbGoals.toString(), data.getInserter(ttrue))

println m

ConfigManager cm = ConfigManager.getManager();
ConfigBundle cb = cm.getBundle("example");
def result = m.mapInference(data.getDatabase(),cb)

result.printAtoms(goal)
//result.getAtoms(goal).each{
    //println it.getArguments()
    //println it.getSoftValues()
//}
