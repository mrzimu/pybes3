#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <string>

#include "Utils.hh"

namespace py = pybind11;

class IBesRootField {
  public:
    virtual void i_fill() = 0;

    virtual void set_status( bool status ) = 0;
    virtual bool get_status()              = 0;
    virtual void clear()                   = 0;

    virtual py::object get_array() = 0;
};

template <typename TSubEvent, typename Record>
/**
 * @brief The BesRootFieldLeaf class represents a leaf field in a ROOT file.
 *
 * This class is an abstract base class that provides an interface for filling and accessing
 * data in a ROOT file. It defines pure virtual functions that must be implemented by derived
 * classes to set up the field map and fill the data array.
 */
class BesRootFieldLeaf : public IBesRootField {
  public:
    /**
     * @brief Constructs a BesRootFieldLeaf object with the given ROOT path.
     *
     * This constructor initializes the BesRootFieldLeaf object with the specified ROOT path.
     *
     * @param rpath The ROOT path of the field.
     */
    BesRootFieldLeaf<TSubEvent, Record>( TSubEvent* obj, const std::string& rpath,
                                         const FieldMap& field_map )
        : m_builder( field_map ), m_rpath( rpath ), m_obj( obj ) {}

    /**
     * @brief Fills the data array.
     *
     * This pure virtual function must be implemented by derived classes to extract event
     * information and fill the data array. It transfers read data from the SubEvent object and
     * writes it to the arrays with the builder.
     */
    virtual void fill() = 0;

    /* ######################################################################################
     */
    /* ######################################################################################
     */

    /**
     * @brief Fills the data if the flag `m_do_fill` is set to true.
     *
     * This function is used by the parent class to fill the data if the flag `m_do_fill` is
     * set to `true`.
     */
    void i_fill() override {
        if ( m_do_fill ) fill();
    }

    /**
     * @brief Sets the fill status.
     *
     * This function sets the fill status to the specified value.
     *
     * @param status The fill status to be set.
     */
    void set_status( bool status ) override { m_do_fill = status; }

    /**
     * @brief Returns the fill status.
     *
     * This function returns the fill status.
     *
     * @return The fill status.
     */
    bool get_status() override { return m_do_fill; }

    /**
     * @brief Clears the builder.
     *
     * This function clears the builder by calling its `clear()` function.
     */
    void clear() override { m_builder.clear(); }

    /**
     * @brief Returns the data array as a Python dictionary.
     *
     * This function returns the data array as a Python dictionary. The dictionary key is the
     * ROOT path of the field, and the value is the snapshot of the builder if the fill status
     * is `true`, or `None` otherwise.
     *
     * @return The data array as a Python dictionary.
     */
    py::object get_array() override {
        return m_do_fill ? snapshot_builder( m_builder ) : py::none();
    }

  protected:
    std::string m_rpath; ///< The ROOT path of the field.

    bool m_do_fill{ true }; ///< The fill status.

    TSubEvent* m_obj{ nullptr }; ///< The TSubEvent pointer.
    Record m_builder;            ///< The builder for the data array.
};