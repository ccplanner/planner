/**
 * 
 */
package edu.umd.cs.chipschallenge

import edu.umd.cs.psl.database.loading.Inserter;

/**
 * Some helper methods for testing.
 *
 */
class TestingUtil {

	/**
	 * Load string as if it were a file.
	 * @param string
	 * @param insert used to load the data
	 */
	public static void loadFromString(String string, Inserter insert){
		def tmp = File.createTempFile("data",null)
		tmp.withWriter{ writer ->
			string.readLines().each {
				writer << it.trim() << "\n"
			}
		}
		insert.loadFromFile(tmp.getCanonicalPath());
	}

	/**
	 * Load string as if it were a file; file contains truth information.
	 * @param string
	 * @param insert used to load the data
	 */
	public static void loadFromStringWithTruth(String string, Inserter insert){
		def tmp = File.createTempFile("data",null)
		tmp.withWriter{ writer ->
			string.readLines().each {
				writer << it.trim() << "\n"
			}
		}
		insert.loadFromFileWithTruth(tmp.getCanonicalPath());
	}

	/**
	 * Load string as if it were a file; file contains true information.
	 * @param string
	 * @param insert
	 * @param delim field delimiter
	 */
	public static void loadFromStringWithTruth(String string, Inserter insert, String delim){
		def tmp = File.createTempFile("data",null)
		tmp.withWriter{ writer ->
			string.readLines().each {
				writer << it.trim() << "\n"
			}
		}
		insert.loadFromFileWithTruth(tmp.getCanonicalPath(), delim);
	}
}
