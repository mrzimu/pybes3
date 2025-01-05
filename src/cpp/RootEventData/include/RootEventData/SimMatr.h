#ifndef SimMatr_h
#define SimMatr_h

namespace SimMat {

    // packing of symmetric matrices 'sm' in one-dimensional array 'pac_sm'
    // 'pac_sm' MUST be large enough to receive n*(n+1)/2 elements
    template <class T>
    inline void pack2d( int n, const T* sm, T* pac_sm ) {
        for ( int i = 0; i < n; i++ )
        {
            for ( int j = 0; j <= i; j++ )
            {
                int k     = i * ( i + 1 ) / 2 + j;
                pac_sm[k] = sm[i * n + j];
            }
        }
    }

    // for a given i and j in 'sm' returns the index in 'pac_sm'
    inline int get_idx( int i, int j ) {
        return ( i > j ) ? i * ( i + 1 ) / 2 + j : j * ( j + 1 ) / 2 + i;
    }

    // for a given i and j return 'sm[i][j]'
    template <class T>
    inline T get_element( const T* pac_sm, int i, int j ) {
        return pac_sm[get_idx( i, j )];
    }

    // unpacks the 'pac_sm' in the symmetric matrix 'sm'
    // 'sm' MUST be large enough to receive n*n elements
    template <class T>
    inline void unpack2d( int n, T* sm, const T* pac_sm ) {
        for ( int i = 0; i < n; i++ )
        {
            for ( int j = 0; j <= i; j++ )
            {
                int k         = i * ( i + 1 ) / 2 + j;
                sm[i * n + j] = sm[i + j * n] = pac_sm[k];
            }
        }
    }

} // namespace SimMat
#endif
