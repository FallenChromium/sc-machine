#ifndef _translator_h_
#define _translator_h_

#include "types.h"

extern "C"
{
#include "sc_memory_headers.h"
#include "sc_helper.h"
}

struct TranslatorParams
{
    //! Name of file to translate
    String fileName;
    //! Flag to generate format information based on file extensions
    bool autoFormatInfo;
};

/*! Interface for translators
 */
class iTranslator
{
public:
    explicit iTranslator();
    virtual ~iTranslator();

    /*! Translate specified file into memory
     * @param params Input parameters
     * @return If file translated without any errors, then returns true; otherwise returns false.
     */
    virtual bool translate(const TranslatorParams &params);

    //! Implementation of translate
    virtual bool translateImpl() = 0;

    //! Returns supported file extension
    virtual const std::string& getFileExt() const = 0;

protected:
    /*! Generates format relation in sc-memory by file extension
     * @param addr sc-addr of sc-link to create format relation
     * @param ext File extension
     */
    void generateFormatInfo(sc_addr addr, const String &ext);

protected:
    //! Translator parameters
    TranslatorParams mParams;

    typedef std::map<String, sc_addr> tStringAddrMap;
    //! Map that contains global identifiers
    static tStringAddrMap msGlobalIdtfAddrs;
    //! Map that contains system identifiers
    tStringAddrMap mSysIdtfAddrs;
    //! Map that contains local identifiers
    tStringAddrMap mLocalIdtfAddrs;
};

/*! Interface for translators factory
 */
class iTranslatorFactory
{
public:
    explicit iTranslatorFactory() {};
    virtual ~iTranslatorFactory() {};

    /*! Function to create translator instance
     */
    virtual iTranslator* createInstance() = 0;

    //! Returns supported file extension
    virtual const std::string& getFileExt() const = 0;
};

#endif // _translator_h_